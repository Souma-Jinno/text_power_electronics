# blfig.py — Blender 版の図で共通に使う部品
# 電磁界理論の教科書（text_electromagnetic_theory/book/figures/blender/lib/blfig.py，2026-10-15 時点）の写し。
# パワエレ教科書の図（fig5.10_miniaturize など）が同じ作り方（Cycles＋Freestyle＋TeX ラベル）で組めるように置く。
# 色の方針（2 色刷り）は電磁界理論の本のもの。パワエレの本ではカラー（本文の図の赤・青）を使ってよい。
#
# 方針（fig1.17_gauss.py と同じ）
#   ・Cycles（Metal GPU）で透明背景にレンダし，build_fig.sh が白に合成する。
#   ・稜線は Freestyle（edge mark のみ。見える稜線＝黒の実線，隠れた稜線＝灰の破線）。
#   ・色は黒・灰・特色の青 RGB(0,0,0.6) の濃淡だけ（2 色刷り）。
#   ・数式ラベルは Blender に入れない。3D の点を投影した画面座標（px）を <名前>.labels.json に書き出し，
#     build_fig.sh が platex（本文と同じ Computer Modern）で重ねる。
#   ・カメラは正投影 1 台。写す範囲は与えた 3D 点の外接長方形＋余白から決め，1 単位の実寸（cm）を固定する。

import bpy
import bmesh
import json
import math
import sys
import time
from pathlib import Path
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

BLUE_SRGB = (0.0, 0.0, 0.6)


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = Path(a[0]).resolve() if a else Path.cwd() / "out"
    samples = int(a[1]) if len(a) > 1 else 128
    out.mkdir(parents=True, exist_ok=True)
    return out, samples


def srgb2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def col(r, g, b, a=1.0):
    return (srgb2lin(r), srgb2lin(g), srgb2lin(b), a)


def blue_tint(t):
    """特色の青の網 t（0=白，1=特色）"""
    return col(1 - t, 1 - t, 1 - 0.4 * t)


class Fig:
    def __init__(self, name, samples, world=0.85):
        self.name = name
        self.t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = self.scene = bpy.context.scene
        sc.render.engine = "CYCLES"
        prefs = bpy.context.preferences.addons["cycles"].preferences
        try:
            prefs.compute_device_type = "METAL"
            prefs.get_devices()
            for d in prefs.devices:
                d.use = True
            sc.cycles.device = "GPU"
        except Exception:
            sc.cycles.device = "CPU"
        sc.cycles.samples = samples
        sc.cycles.use_denoising = True
        sc.cycles.transparent_max_bounces = 32
        sc.cycles.max_bounces = 6
        sc.render.film_transparent = True
        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
        sc.render.image_settings.file_format = "PNG"
        sc.render.image_settings.color_mode = "RGBA"
        w = bpy.data.worlds.new("W")
        sc.world = w
        w.use_nodes = True
        bg = w.node_tree.nodes["Background"]
        bg.inputs["Color"].default_value = (1, 1, 1, 1)
        bg.inputs["Strength"].default_value = world
        self.lines = bpy.data.collections.new("Lines")      # Freestyle の対象
        self.other = bpy.data.collections.new("Other")
        sc.collection.children.link(self.lines)
        sc.collection.children.link(self.other)
        self.labels = []

    # ---------------- マテリアル ----------------
    def glass(self, name, tint, milk=0.16, rough=0.25, ior=1.25):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        tr.inputs["Color"].default_value = tint
        df = nt.nodes.new("ShaderNodeBsdfDiffuse")
        df.inputs["Color"].default_value = tint
        gl = nt.nodes.new("ShaderNodeBsdfGlossy")
        gl.inputs["Roughness"].default_value = rough
        m1 = nt.nodes.new("ShaderNodeMixShader")
        m1.inputs["Fac"].default_value = milk
        nt.links.new(tr.outputs[0], m1.inputs[1])
        nt.links.new(df.outputs[0], m1.inputs[2])
        fr = nt.nodes.new("ShaderNodeFresnel")
        fr.inputs["IOR"].default_value = ior
        m2 = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(fr.outputs[0], m2.inputs["Fac"])
        nt.links.new(m1.outputs[0], m2.inputs[1])
        nt.links.new(gl.outputs[0], m2.inputs[2])
        nt.links.new(m2.outputs[0], out.inputs[0])
        return m

    def solid(self, name, c, emit=0.3, rough=0.45, metallic=0.0):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        p = m.node_tree.nodes["Principled BSDF"]
        p.inputs["Base Color"].default_value = c
        p.inputs["Roughness"].default_value = rough
        p.inputs["Metallic"].default_value = metallic
        p.inputs["Emission Color"].default_value = c
        p.inputs["Emission Strength"].default_value = emit
        return m

    # ---------------- 形 ----------------
    def _link(self, o, coll):
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)

    def mesh(self, name, verts, faces, mats, fidx=None, mark_edges=True, coll=None, smooth=False):
        """任意のメッシュ。mark_edges=True なら全稜線を Freestyle の edge mark にする"""
        me = bpy.data.meshes.new(name)
        me.from_pydata([tuple(v) for v in verts], [], faces)
        me.update()
        for m in mats:
            me.materials.append(m)
        if fidx is not None:
            for p, i in zip(me.polygons, fidx):
                p.material_index = i
        if smooth:
            for p in me.polygons:
                p.use_smooth = True
        if mark_edges:
            self.mark_all(me)
        ob = bpy.data.objects.new(name, me)
        (coll or (self.lines if mark_edges else self.other)).objects.link(ob)
        return ob

    @staticmethod
    def mark_all(me, pred=None):
        idx = [i for i, e in enumerate(me.edges) if pred is None or pred(e)]
        try:
            for i in idx:
                me.edges[i].use_freestyle_mark = True
        except AttributeError:
            at = me.attributes.get("freestyle_edge") or me.attributes.new("freestyle_edge", "BOOLEAN", "EDGE")
            for i in idx:
                at.data[i].value = True

    def box(self, name, lo, hi, mat, mark=True):
        x0, y0, z0 = lo
        x1, y1, z1 = hi
        V = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
             (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        return self.mesh(name, V, F, [mat], mark_edges=mark)

    def tube(self, name, pts, radius, mat, coll=None, res=10):
        """点列を通る細いチューブ（ベジエでなくポリライン＋ベベル）"""
        cu = bpy.data.curves.new(name, "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = radius
        cu.bevel_resolution = 4
        cu.use_fill_caps = True
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        for p, q in zip(sp.points, pts):
            p.co = (q[0], q[1], q[2], 1)
        cu.materials.append(mat)
        ob = bpy.data.objects.new(name, cu)
        (coll or self.other).objects.link(ob)
        return ob

    def cone(self, tip, u, length, radius, mat, coll=None):
        u = Vector(u).normalized()
        rot = u.to_track_quat("Z", "Y").to_matrix().to_4x4()
        bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=radius, radius2=0, depth=length)
        o = bpy.context.active_object
        o.matrix_world = Matrix.Translation(Vector(tip) - u * length / 2) @ rot
        o.data.materials.append(mat)
        self._smooth(o)
        self._link(o, coll or self.other)
        return o

    def _smooth(self, o):
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.shade_smooth()

    def arrow(self, p, q, mat, r_shaft, head_l, r_head, coll=None):
        """円柱（軸）＋円錐（矢じり）"""
        p, q = Vector(p), Vector(q)
        d = q - p
        u = d.normalized()
        L = d.length
        rot = u.to_track_quat("Z", "Y").to_matrix().to_4x4()
        ls = max(L - head_l * 0.9, 1e-4)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=r_shaft, depth=ls)
        sh = bpy.context.active_object
        sh.matrix_world = Matrix.Translation(p + u * ls / 2) @ rot
        sh.data.materials.append(mat)
        self._smooth(sh)
        self._link(sh, coll or self.other)
        self.cone(q, u, head_l, r_head, mat, coll)

    def curve_arrow(self, pts, mat, r_shaft, head_l, r_head, coll=None):
        """曲線に沿う矢印：点列の終点に矢じり（点列は矢じりの長さだけ手前で止める）"""
        pts = [Vector(p) for p in pts]
        # 終点から head_l だけ戻った所まで軸を描く
        acc, k = 0.0, len(pts) - 1
        while k > 0 and acc + (pts[k] - pts[k - 1]).length < head_l * 0.9:
            acc += (pts[k] - pts[k - 1]).length
            k -= 1
        shaft = pts[:k + 1]
        self.tube("carrow", shaft, r_shaft, mat, coll)
        u = (pts[-1] - pts[k]).normalized()
        self.cone(pts[-1], u, head_l, r_head, mat, coll)

    def torus(self, name, center, axis, R, r, mat, coll=None):
        bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=128, minor_segments=24)
        o = bpy.context.active_object
        rot = Vector(axis).normalized().to_track_quat("Z", "Y").to_matrix().to_4x4()
        o.matrix_world = Matrix.Translation(Vector(center)) @ rot
        o.data.materials.append(mat)
        self._smooth(o)
        self._link(o, coll or self.other)
        return o

    # ---------------- 光・カメラ ----------------
    def area_light(self, loc, target, size=9, energy=900):
        bpy.ops.object.light_add(type="AREA", location=loc)
        L = bpy.context.active_object
        L.data.size = size
        L.data.energy = energy
        L.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
        return L

    def camera(self, view_dir, pts, unit_cm, dpi=600, margin=0.12, up_hint=(0, 0, 1)):
        """正投影。view_dir はカメラの位置の向き（被写体からカメラへ）。pts が全部入るように範囲を決める"""
        v = Vector(view_dir).normalized()
        right = Vector(up_hint).cross(v).normalized()
        up = v.cross(right).normalized()
        xs = [Vector(p).dot(right) for p in pts]
        ys = [Vector(p).dot(up) for p in pts]
        x0, x1 = min(xs) - margin, max(xs) + margin
        y0, y1 = min(ys) - margin, max(ys) + margin
        wid, hei = x1 - x0, y1 - y0
        center = right * (x0 + x1) / 2 + up * (y0 + y1) / 2
        cd = bpy.data.cameras.new("cam")
        cd.type = "ORTHO"
        cd.ortho_scale = max(wid, hei)
        cd.clip_start = 0.1
        cd.clip_end = 200
        cam = bpy.data.objects.new("cam", cd)
        self.scene.collection.objects.link(cam)
        cam.location = center + v * 50
        cam.rotation_euler = (-v).to_track_quat("-Z", "Y").to_euler()
        self.scene.camera = cam
        ppu = unit_cm / 2.54 * dpi
        self.scene.render.resolution_x = round(wid * ppu)
        self.scene.render.resolution_y = round(hei * ppu)
        self.scene.render.resolution_percentage = 100
        self.dpi = dpi
        self.cam, self.right, self.up, self.view = cam, right, up, v
        bpy.context.view_layer.update()
        return cam

    def screen_dir(self, d):
        """3D の向き d の画面上の向き（右, 上）"""
        d = Vector(d)
        return (d.dot(self.right), d.dot(self.up))

    # ---------------- Freestyle ----------------
    def freestyle(self, front_pt=0.55, hidden_pt=0.4, hidden=True, hidden_gray=0.45, sil=None, sil_pt=0.35, sil_color=(0.3, 0.3, 0.3)):
        """sil：輪郭線（silhouette・border）だけを描くコレクション（半透明の曲面の形を見せる用）"""
        sc = self.scene
        sc.render.use_freestyle = True
        sc.render.line_thickness_mode = "ABSOLUTE"
        vl = bpy.context.view_layer
        vl.use_freestyle = True
        fs = vl.freestyle_settings
        fs.crease_angle = math.radians(179)
        for ls in list(fs.linesets):
            fs.linesets.remove(ls)

        def mk(name, vis, color, thick, dashed, coll=None, types=("select_edge_mark",)):
            ls = fs.linesets.new(name)
            ls.select_by_visibility = True
            ls.visibility = vis
            ls.select_by_edge_types = True
            ls.select_by_collection = True
            ls.collection = coll or self.lines
            for a in ("select_silhouette", "select_border", "select_crease", "select_contour",
                      "select_external_contour", "select_material_boundary", "select_suggestive_contour",
                      "select_ridge_valley"):
                if hasattr(ls, a):
                    setattr(ls, a, False)
            ls.select_edge_mark = False
            for t in types:
                setattr(ls, t, True)
            st = ls.linestyle
            st.color = color
            st.thickness = thick
            st.thickness_position = "CENTER"
            st.caps = "ROUND"
            st.chaining = "PLAIN"
            st.use_chain_count = False
            if dashed:
                st.use_dashed_line = True
                st.dash1, st.gap1 = 14, 12

        mk("front", "VISIBLE", (0, 0, 0), front_pt / 72 * self.dpi, False)
        if sil is not None:
            mk("sil", "VISIBLE", sil_color, sil_pt / 72 * self.dpi, False, coll=sil,
               types=("select_silhouette", "select_border"))
        if hidden:
            g = hidden_gray
            mk("hidden", "HIDDEN", (g, g, g), hidden_pt / 72 * self.dpi, True)

    # ---------------- ラベル ----------------
    def proj(self, p):
        sc = self.scene
        c = world_to_camera_view(sc, self.cam, Vector(p))
        return (c.x * sc.render.resolution_x, (1 - c.y) * sc.render.resolution_y)

    def label(self, p, tex, anchor="center", dx=0.0, dy=0.0, color=None):
        """3D 点 p に TeX ラベル。anchor は TikZ の anchor，dx, dy は bp 単位のずらし（右・上が正）"""
        x, y = self.proj(p)
        if color == "blue":
            tex = r"\textcolor{accent}{" + tex + "}"
        elif color == "white":
            tex = r"\textcolor{white}{" + tex + "}"
        self.labels.append(dict(tex=tex, x=x, y=y, anchor=anchor, dx=dx, dy=dy))

    # ---------------- 書き出し ----------------
    def render(self, out, extra=None):
        sc = self.scene
        RX, RY = sc.render.resolution_x, sc.render.resolution_y
        J = dict(width_px=RX, height_px=RY, dpi=self.dpi, labels=self.labels)
        (out / f"{self.name}.labels.json").write_text(json.dumps(J, ensure_ascii=False, indent=1))
        if extra is not None:
            (out / f"{self.name}.geom.json").write_text(json.dumps(extra, ensure_ascii=False, indent=1))
        sc.render.filepath = str(out / f"_{self.name}.render.png")
        t1 = time.time()
        bpy.ops.render.render(write_still=True)
        print(f"RENDER_DONE {RX}x{RY} samples={sc.cycles.samples} build={t1 - self.t0:.1f}s render={time.time() - t1:.1f}s")


def _frame(axis):
    """軸 axis に垂直な正規直交基底 (e1, e2)"""
    a = Vector(axis).normalized()
    h = Vector((0, 0, 1)) if abs(a.z) < 0.9 else Vector((1, 0, 0))
    e1 = a.cross(h).normalized()
    e2 = a.cross(e1).normalized()
    return a, e1, e2


def cyl_solid(F, name, p0, p1, r_in, r_out, mat, n=96, mark=True, coll=None):
    """p0→p1 を軸とする円柱（r_in=0）または肉厚の円筒（r_in>0）。両端の円の縁だけを Freestyle の稜線にする"""
    p0, p1 = Vector(p0), Vector(p1)
    a, e1, e2 = _frame(p1 - p0)
    V, Fc = [], []
    circ = lambda c, r: [c + r * (math.cos(2 * math.pi * i / n) * e1 + math.sin(2 * math.pi * i / n) * e2) for i in range(n)]
    if r_in <= 0:
        V = circ(p0, r_out) + circ(p1, r_out)
        Fc.append(tuple(range(n))[::-1])
        Fc.append(tuple(n + i for i in range(n)))
        Fc += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        rim = lambda e: (e.vertices[0] < n) == (e.vertices[1] < n) and abs(e.vertices[0] - e.vertices[1]) in (1, n - 1)
    else:
        V = circ(p0, r_out) + circ(p1, r_out) + circ(p0, r_in) + circ(p1, r_in)
        o0, o1, i0, i1 = 0, n, 2 * n, 3 * n
        for i in range(n):
            j = (i + 1) % n
            Fc += [(o0 + i, o0 + j, o1 + j, o1 + i), (i0 + j, i0 + i, i1 + i, i1 + j),
                   (o0 + j, o0 + i, i0 + i, i0 + j), (o1 + i, o1 + j, i1 + j, i1 + i)]
        rim = lambda e: (e.vertices[0] // n) == (e.vertices[1] // n)
    ob = F.mesh(name, [tuple(v) for v in V], Fc, [mat], mark_edges=False, coll=coll, smooth=False)
    for p in ob.data.polygons:
        p.use_smooth = abs(p.normal.dot(a)) < 0.5      # 側面だけなめらかに（端面は平ら）
    if mark:
        F.mark_all(ob.data, pred=rim)
        if coll is None:
            F._link(ob, F.lines)
    return ob


def circle_pts(c, axis, r, n=161, a0=0.0, a1=2 * math.pi):
    c = Vector(c)
    a, e1, e2 = _frame(axis)
    return [c + r * (math.cos(t) * e1 + math.sin(t) * e2) for t in (a0 + (a1 - a0) * k / (n - 1) for k in range(n))]


# ---------------- 追加（2026-09-30）：破線のチューブ・球・平らな多角形 ----------------
def dashed_tube(F, name, pts, radius, mat, dash=0.06, gap=0.045, coll=None):
    """点列を弧長で dash・gap に切った破線のチューブ（補助線・投影線用）"""
    pts = [Vector(p) for p in pts]
    segs, cur, s, on = [], [pts[0]], 0.0, True
    per = dash
    for a, b in zip(pts[:-1], pts[1:]):
        L = (b - a).length
        t = 0.0
        while L - t > 1e-9:
            step = min(per - s, L - t)
            t += step
            s += step
            p = a + (b - a) * (t / L)
            if on:
                cur.append(p)
            if s >= per - 1e-9:
                if on and len(cur) > 1:
                    segs.append(cur)
                on = not on
                s = 0.0
                per = dash if on else gap
                cur = [p]
    if on and len(cur) > 1:
        segs.append(cur)
    return [F.tube(name, sg, radius, mat, coll) for sg in segs]


def ball(F, name, c, r, mat, coll=None, seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=tuple(c), segments=seg, ring_count=seg // 2)
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(mat)
    F._smooth(o)
    F._link(o, coll or F.other)
    return o


def flat_poly(F, name, pts, mat, mark=True, coll=None):
    """平らな多角形 1 枚（縁を Freestyle の稜線にする）"""
    return F.mesh(name, [tuple(p) for p in pts], [tuple(range(len(pts)))], [mat], mark_edges=mark, coll=coll)


def half_shell(F, name, center, r_in, r_out, mat, nth=64, nph=96, mark=True):
    """奥の半分（y ≥ 0）だけの肉厚の球殻（r_in=0 なら中身の詰まった半球）。切り口 y=0 の面（輪）も張る。
    切り口の縁（r_in・r_out の半円）と，外側の球面の縁を Freestyle の稜線にする"""
    c = Vector((0, 0, 0))          # 原点で作ってから object を center へ動かす（大きな座標での丸め誤差を避ける）
    V, Fc = [], []

    def hemi(r, flip):
        base = len(V)
        # θ：z 軸からの角（0..π），φ：0..π（y ≥ 0 の半分，x = r sinθ cosφ, y = r sinθ sinφ）
        for i in range(nth + 1):
            th = math.pi * i / nth
            for j in range(nph + 1):
                ph = math.pi * j / nph
                V.append(tuple(c + Vector((r * math.sin(th) * math.cos(ph), r * math.sin(th) * math.sin(ph), r * math.cos(th)))))
        for i in range(nth):
            for j in range(nph):
                a, b = base + i * (nph + 1) + j, base + i * (nph + 1) + j + 1
                d, e = base + (i + 1) * (nph + 1) + j, base + (i + 1) * (nph + 1) + j + 1
                f = (a, d, e, b) if not flip else (a, b, e, d)
                Fc.append(f)
        return base

    bo = hemi(r_out, False)
    bi = hemi(r_in, True) if r_in > 0 else None
    # 切り口：φ = 0 と φ = π の半円を内外でつなぐ
    if bi is not None:
        for i in range(nth):
            for j in (0, nph):
                o1, o2 = bo + i * (nph + 1) + j, bo + (i + 1) * (nph + 1) + j
                i1, i2 = bi + i * (nph + 1) + j, bi + (i + 1) * (nph + 1) + j
                Fc.append((o1, o2, i2, i1) if j == 0 else (o1, i1, i2, o2))
    else:
        # 中身の詰まった半球：切り口は半円板（中心点で扇に張る）
        V.append(tuple(c))
        cc = len(V) - 1
        for i in range(nth):
            for j in (0, nph):
                o1, o2 = bo + i * (nph + 1) + j, bo + (i + 1) * (nph + 1) + j
                Fc.append((o1, o2, cc) if j == 0 else (o2, o1, cc))
    ob = F.mesh(name, V, Fc, [mat], mark_edges=False, smooth=False)
    ob.location = Vector(center)
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=1e-6)
    bpy.ops.object.mode_set(mode="OBJECT")
    me = ob.data
    # 切り口の面 = 頂点がすべて y = c.y にある面（法線で判定すると球面の最も奥の面も拾ってしまう）
    flat = [all(abs(me.vertices[v].co.y - c.y) < 1e-6 for v in p.vertices) for p in me.polygons]
    for p, fl in zip(me.polygons, flat):
        p.use_smooth = not fl
    if mark:
        # 切り口（y = 0 の面）の縁と，球面との境 = 平らな面と曲面の境の辺
        ek_flat, ek_curved = set(), set()
        for p, fl in zip(me.polygons, flat):
            (ek_flat if fl else ek_curved).update(p.edge_keys)
        border = ek_flat & ek_curved
        F.mark_all(me, pred=lambda e: tuple(sorted(e.vertices)) in border)
        F._link(ob, F.lines)
    return ob

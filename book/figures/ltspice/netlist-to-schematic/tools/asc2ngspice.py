# -*- coding: utf-8 -*-
"""
asc2ngspice.py  --  Faithful LTspice .asc -> ngspice .cir emitter.

Uses .asy PIN definitions (load_asy) and a union-find netlister (like
tools_ascnet_check.parse) but adds:
  * jumper (Misc\\jumper) pin-shorting
  * SYMATTR Value / Value2 / SpiceLine / SpiceLine2 extraction.  Rser/Lser are
    expanded into explicit elements; EVERY other key is carried verbatim onto
    the element card and any SYMATTR this file does not understand is refused
    outright (2026-09-04 audit hole B1 -- they used to be dropped in silence)
  * TEXT '!' directive extraction (.model/.param/.options/.tran/K...)
  * expansion of LTspice Rser/Lser (unsupported by ngspice) into explicit
    series R / L elements (dot terminal of L preserved for K coupling)
  * pi param injection, param topological sort, .tran translation
  * ngspice convergence aids (itl4/trtol) emitted as DEFAULTS: only for keys
    the .asc does not set itself, so the schematic's own .options always win
    (--legacy-options restores the old unconditional override)

Pin order per symbol == PINATTR SpiceOrder (parsed since 2026-09-04; PIN file
order is used only when the .asy states no SpiceOrder, and that is announced).
  res/cap/ind/ind2 : A(1) B(2)
  diode            : +anode(1) -cathode(2)   -> D name anode cathode model
  voltage          : +(1) -(2)               -> V name + - value
  sw               : A(1) B(2) NC+(3) NC-(4)  -> S name A B NC+ NC- model
  jumper           : +(1) -(2)               -> short (no element)
"""
import sys, os, re, glob
from collections import defaultdict

ORI = {'R0':lambda x,y:(x,y),'R90':lambda x,y:(-y,x),'R180':lambda x,y:(-x,-y),
       'R270':lambda x,y:(y,-x),'M0':lambda x,y:(-x,y),'M90':lambda x,y:(y,x),
       'M180':lambda x,y:(x,-y),'M270':lambda x,y:(-y,-x)}

def load_asy(libdir, messages=None):
    """symbol key -> [(px,py), ...] in SPICE terminal order.

    2026-09-04 audit fix (A2).  Until this date the loader used the FILE ORDER
    of the `PIN` lines and merely *assumed* it equalled `PINATTR SpiceOrder`.
    That is what LTspice itself does NOT do: LTspice writes a symbol's
    terminals into the netlist in SpiceOrder, and a perfectly legal .asy may
    list its PIN records in any order.  All ten symbols shipped in ltsym/
    happen to agree, so nothing was broken -- but a tampered voltage.asy whose
    two PIN blocks are swapped (SpiceOrder 2 first, 1 second) silently
    reversed the polarity of EVERY voltage source and the round trip still
    said PASS, because both directions of the round trip used the same wrong
    order.  Pins are now sorted by SpiceOrder.

    `messages` (optional list) collects human-readable NOTE/WARNING strings:
      * NOTE    -- a symbol has no SpiceOrder at all: file order is used, which
                   is a guess.
      * WARNING -- file order and SpiceOrder disagree (legal, but surprising);
                   SpiceOrder wins.
      * WARNING -- SpiceOrder values are duplicated/unusable: file order is
                   kept and the fact is said out loud.
    """
    pins = {}
    msgs = messages if messages is not None else []
    files = sorted(set(glob.glob(os.path.join(libdir,'**','*.asy'),recursive=True) +
                       glob.glob(os.path.join(libdir,'*.asy'))))
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0].lower()
        try: txt = open(f, encoding='utf-16').read()
        except Exception:
            try: txt = open(f, encoding='latin-1').read()
            except Exception: continue
        pl = []            # [x, y, spiceorder-or-None] in .asy FILE order
        for ln in txt.splitlines():
            p = ln.split()
            if p[:1] == ['PIN']:
                pl.append([int(p[1]), int(p[2]), None])
            elif (p[:1] == ['PINATTR'] and len(p) >= 3 and pl
                  and p[1].lower() == 'spiceorder'):
                try: pl[-1][2] = int(p[2])
                except ValueError:
                    msgs.append('WARNING: %s: PINATTR SpiceOrder %r is not an '
                                'integer; ignored' % (os.path.basename(f), p[2]))
        orders = [q[2] for q in pl]
        ordered = pl
        if pl and all(o is not None for o in orders):
            if len(set(orders)) != len(orders):
                msgs.append('WARNING: %s: PINATTR SpiceOrder values %s are not '
                            'unique; falling back to PIN file order, terminal '
                            'order for this symbol is a GUESS'
                            % (os.path.basename(f), orders))
            else:
                ordered = sorted(pl, key=lambda q: q[2])
                if ordered != pl:
                    msgs.append('WARNING: %s: PIN file order and PINATTR '
                                'SpiceOrder disagree (SpiceOrder of the PIN '
                                'lines, in file order, is %s); using SpiceOrder '
                                '-- that is what LTspice netlists'
                                % (os.path.basename(f), orders))
        elif pl:
            miss = sum(1 for o in orders if o is None)
            msgs.append('NOTE: %s: %d of %d PIN record(s) carry no PINATTR '
                        'SpiceOrder; using PIN file order for this symbol, '
                        'which is an ASSUMPTION, not information from the .asy'
                        % (os.path.basename(f), miss, len(pl)))
        pins[name] = [(q[0], q[1]) for q in ordered]
    return pins

def on_seg(p, a, b):
    (px,py),(ax,ay),(bx,by) = p, a, b
    if ax==bx==px and min(ay,by)<=py<=max(ay,by): return True
    if ay==by==py and min(ax,bx)<=px<=max(ax,bx): return True
    return False

def symkey(raw):
    """normalise SYMBOL name to an .asy key ('misc\\jumper' or 'jumper' -> 'jumper')."""
    k = raw.lower().replace('\\\\','\\')
    if 'jumper' in k: return 'jumper'
    if '\\' in k: k = k.split('\\')[-1]
    return k

def parse_asc(ascfile, pins):
    raw = open(ascfile, 'rb').read()
    # LTspice は UTF-16LE(BOMなし) と UTF-8 の両方を書く。BOM と NUL の有無で見分ける。
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
        txt = raw.decode('utf-16')
    elif b'\x00' in raw[:200]:
        txt = raw.decode('utf-16-le')
    else:
        txt = raw.decode('utf-8')
    s = txt.replace('\r\n','\n').split('\n')
    wires=[]; flags=[]; syms=[]; directives=[]
    cur=None
    def flush(cur):
        if cur is not None and cur.get('InstName'):
            syms.append(cur)
    i=0
    while i < len(s):
        ln = s[i]; p = ln.split()
        head = p[0] if p else ''
        if head=='WIRE':
            wires.append(((int(p[1]),int(p[2])),(int(p[3]),int(p[4]))))
        elif head=='FLAG':
            flags.append(((int(p[1]),int(p[2])), ln.split(' ',3)[3]))
        elif head=='SYMBOL':
            flush(cur)
            cur={'rawsym':p[1],'sym':symkey(p[1]),'x':int(p[2]),'y':int(p[3]),'ori':p[4]}
        elif head=='SYMATTR' and cur is not None:
            parts = ln.split(None,2)
            if len(parts)>=3:
                cur[parts[1]] = parts[2]
                # keep the KEY NAMES too, in file order.  emit_devices() has to
                # be able to tell "this symbol carries an attribute I do not
                # understand" from "this symbol carries nothing", and cur is
                # also used for bookkeeping keys of our own ('sym', 'ori', ...)
                # so its plain key set cannot answer that (2026-09-04, hole B1).
                cur.setdefault('_symattr', []).append(parts[1])
        elif head=='TEXT':
            # TEXT x y Just Size <text...>
            parts = ln.split(None,5)
            if len(parts)>=6:
                body = parts[5]
                if body.startswith('!'):
                    for dl in body[1:].split('\\n'):
                        dl=dl.strip()
                        if dl: directives.append(dl)
            flush(cur); cur=None
        elif head in ('WINDOW',):
            pass  # stays inside current symbol block
        elif head in ('LINE','RECTANGLE','CIRCLE','ARC','DATAFLAG','BUSTAP',
                      'SHEET','Version','IOPIN','BUSDATA'):
            flush(cur); cur=None
        i+=1
    flush(cur)

    # ---- union-find over integer coordinates ----
    parent={}
    def find(a):
        parent.setdefault(a,a)
        while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
        return a
    def union(a,b):
        parent.setdefault(a,a); parent.setdefault(b,b); parent[find(a)]=find(b)
    for a,b in wires: union(a,b)

    # symbol pins in global coords
    allpins=[]  # (inst, sym, k, coord)
    for cur in syms:
        t=ORI.get(cur['ori'],ORI['R0']); x,y=cur['x'],cur['y']
        pl=pins.get(cur['sym'],[])
        coords=[]
        for k,(rx,ry) in enumerate(pl):
            dx,dy=t(rx,ry); c=(x+dx,y+dy)
            parent.setdefault(c,c); coords.append(c)
            allpins.append((cur['InstName'],cur['sym'],k,c))
        cur['pincoords']=coords

    # ---- LTspice contact semantics (2026-08-27 audit fix) ----
    # Until 2026-08-27 this netlister unioned only (a) the two endpoints of a
    # wire and (b) a SYMBOL PIN lying on a wire.  LTspice connects strictly
    # more than that: ANY point of interest that lies ON a wire -- including
    # in the INTERIOR of the segment -- is on that wire's net.  The two cases
    # that were missed:
    #   * a WIRE ENDPOINT landing mid-segment on another wire  (a T junction)
    #   * a FLAG placed mid-segment on a wire  (LTspice attaches a label
    #     anywhere along the wire, not just at its ends)
    # Both were proven to hide a dead short (audit_fable/corrupt_B_tjunction.asc
    # and audit_fable/corrupt_A_midflag.asc).  net2asc.py's geometric_check()
    # had modelled them all along, i.e. the safety net was stronger than the
    # netlister it was supposed to be checked against.  Points are visited in
    # sorted order so the resulting partition (and hence the emitted deck) is
    # deterministic.
    pts=set()
    for a,b in wires: pts.add(a); pts.add(b)
    for inst,sym,k,c in allpins: pts.add(c)
    for c,nm in flags: pts.add(c)
    for c in sorted(pts):
        for a,b in wires:
            if c==a or c==b or on_seg(c,a,b): union(c,a)

    # jumper: short its two pins together (it is pure wiring)
    for cur in syms:
        if cur['sym']=='jumper' and len(cur['pincoords'])==2:
            union(cur['pincoords'][0], cur['pincoords'][1])

    # ---- net LABELS are GLOBAL (2026-08-27 audit fix) ----
    # In LTspice (and in ngspice, where node names are case-insensitive) two
    # wires carrying the same label are ONE net even if no copper joins them.
    # The old code got this right only by accident: it gave both components
    # the same node NAME, so ngspice merged them downstream.  Doing the union
    # explicitly is what makes the *converse* case visible: when ONE component
    # carries TWO different labels, those two names are aliases of each other,
    # so every net with either name collapses into a single node.  That is the
    # signature of a mid-wire FLAG short, and printing it as one node is what
    # lets net2asc.py's round-trip comparison see the damage.
    for c,nm in flags: parent.setdefault(c,c)
    bylabel={}
    for c,nm in flags:
        bylabel.setdefault(nm.lower(),[]).append(c)
    for key in sorted(bylabel):
        cs=bylabel[key]
        for c in cs[1:]: union(cs[0],c)

    # flags -> net names (after every union, so a component sees ALL its names)
    netname=defaultdict(set)
    for c,nm in flags:
        netname[find(c)].add(nm)

    # components carrying more than one DISTINCT name (case-insensitively):
    # report them so a caller can fail on an accidental short.
    aliases=[]
    for r,nms in netname.items():
        if len({n.lower() for n in nms})>1:
            aliases.append(sorted(nms))
    aliases.sort()

    # assign a clean node name to each root.
    # The invented names for unnamed junctions ('n1', 'n2', ...) must not
    # collide with a name the schematic itself uses, or a reconstructed
    # junction silently fuses with a real net.  ngspice node names are
    # case-insensitive, so the taken-set is compared case-insensitively too
    # (2026-08-27: this hazard was documented in NET2ASC.md 5B.6 and worked
    # around on the net2asc.py side by labelling every drawn net; it is now
    # handled here, at its source).
    taken={re.sub(r'[^A-Za-z0-9_]','_',nm).lower() for _,nm in flags}
    rootname={}; seq=[0]
    def node_of(c):
        r=find(c)
        if r in rootname: return rootname[r]
        nms=netname.get(r)
        if nms and '0' in nms:
            name='0'
        elif nms:
            raw=sorted(nms)[0]
            name=re.sub(r'[^A-Za-z0-9_]','_',raw)
        else:
            while True:
                seq[0]+=1; name='n%d'%seq[0]
                if name.lower() not in taken: break
        rootname[r]=name; return name

    return syms, allpins, node_of, find, directives, aliases


def contact_report(ascfile, libdir, messages=None):
    """Alias groups found by the LTspice contact analysis of an .asc.

    Returns a list of sorted name lists; each entry is one electrical
    component that carries more than one distinct net label -- i.e. those
    names are the SAME node.  An empty list means every component has at most
    one name.  Used by net2asc.py --check."""
    pins=load_asy(libdir, messages)
    return parse_asc(ascfile, pins)[5]


def directive_report(ascfile, libdir, messages=None):
    """The '!' SPICE-directive lines an .asc carries, verbatim and in order.

    This is what LTspice hands to the simulator on top of the drawn symbols:
    dot cards (.tran/.ic/.model/...), K coupling statements, and element cards
    for devices that have no symbol (B/E/G/F/H).  Used by net2asc.py to compare
    the SET of directives against the input deck -- the emitted round-trip deck
    cannot be used for that, because emit() rewrites .tran, re-orders .param
    and injects .options aids (2026-09-04, hole B3)."""
    pins=load_asy(libdir, messages)
    return parse_asc(ascfile, pins)[4]

# ---------------- emission ----------------
def fmt_val(v):
    return v.strip() if v else v

_SL_KV = re.compile(r'(\w+)\s*=\s*(\S+)')

def parse_spiceline(sl):
    """return dict of key->value from a SpiceLine like 'Rser=6.24m Lser=10n'."""
    d={}
    if not sl: return d
    for m in _SL_KV.finditer(sl):
        d[m.group(1).lower()]=m.group(2)
    return d

def spiceline_leftover(sl, consumed):
    """Everything in a SpiceLine that `consumed` did not account for.

    2026-09-04 audit, hole B1.  parse_spiceline() picked `rser`/`lser` out of
    the SpiceLine and the caller then **silently discarded every other key**.
    LTspice does not discard them: it netlists a symbol as

        <name> <nodes> <Value> <Value2> <SpiceLine> <SpiceLine2>

    so `SYMATTR SpiceLine Rpar=0.001` on a capacitor is a 1 mOhm resistor
    ACROSS that capacitor -- a dead short.  Because the extracted deck never
    mentioned it, net2asc.py's round-trip comparison could not see it and
    --check answered `VERIFY: PASS`, exit 0.

    Unconsumed text (key=value pairs and any free text between them) is now
    returned verbatim, in source order, so the caller can put it back on the
    card.  That is what makes the tampering visible to the value comparison --
    the fix is 'stop dropping things', not 'know about Rpar'."""
    if not sl:
        return ''
    out=[]; pos=0
    for m in _SL_KV.finditer(sl):
        free=sl[pos:m.start()].strip()
        if free: out.append(free)
        if m.group(1).lower() not in consumed:
            out.append('%s=%s'%(m.group(1),m.group(2)))
        pos=m.end()
    free=sl[pos:].strip()
    if free: out.append(free)
    return ' '.join(out)

# SYMATTR keys this extractor knows what to do with.  LTspice writes exactly
# these into a SYMBOL block of an .asc, and all of them (except InstName, which
# becomes the element name) end up on the element card.  Anything else is
# REFUSED rather than ignored: an attribute that we cannot place is an
# attribute we would be dropping, and dropping is precisely the defect this
# check exists to stop.
KNOWN_SYMATTR = {'instname', 'value', 'value2', 'spiceline', 'spiceline2'}

def _card_tail(cur, consumed, msgs):
    """The `<Value2> <SpiceLine> <SpiceLine2>` tail LTspice appends to a card.

    `consumed` is the set of SpiceLine keys the caller turned into explicit
    elements (Rser/Lser), or None when the caller used the whole SpiceLine
    itself (an X subcircuit call).  Everything left over is returned with a
    leading space, ready to append, and announced as a WARNING -- it is part
    of the circuit, it is not expanded, and ngspice may not understand it."""
    used=[]; parts=[]
    v2=(cur.get('Value2') or '').strip()
    if v2: parts.append(v2); used.append('Value2')
    if consumed is not None:
        left=spiceline_leftover(cur.get('SpiceLine'), consumed)
        if left: parts.append(left); used.append('SpiceLine')
    sl2=(cur.get('SpiceLine2') or '').strip()
    if sl2: parts.append(sl2); used.append('SpiceLine2')
    if not parts:
        return ''
    if msgs is not None:
        msgs.append('WARNING: %s: SYMATTR %s (%s) is appended to the element '
                    'card by LTspice, so it IS part of the circuit.  It is '
                    'carried through verbatim, NOT expanded into explicit '
                    'elements, and ngspice may not understand every key.'
                    % (cur.get('InstName'), '/'.join(used), ' '.join(parts)))
    return ' '+' '.join(parts)

def _check_symattr(cur, msgs):
    """Refuse any SYMATTR this extractor cannot account for (hole B1)."""
    if msgs is None:
        return
    for k in cur.get('_symattr', ()):
        if k.lower() not in KNOWN_SYMATTR:
            msgs.append('ERROR: %s: SYMATTR %s is not understood by '
                        'asc2ngspice.py.  It is NOT carried into the extracted '
                        'netlist, so the round-trip comparison cannot see what '
                        'it does; refusing rather than dropping it in silence.'
                        % (cur.get('InstName'), k))

TYPELET={'res':'R','cap':'C','ind':'L','ind2':'L','diode':'D','voltage':'V','sw':'S'}
def ename(sym,inst):
    """ngspice element name: LTspice InstName already starts with the type
    letter (Lm1, Cce1, Rg1, Vg1, S1, D1); only prefix if it doesn't."""
    L=TYPELET[sym]
    return inst if inst[:1].upper()==L else L+inst

def emit_devices(syms, node_of, msgs=None):
    lines=[]; seq=[0]
    def newnode(inst):
        seq[0]+=1; return 'x%s_%d'%(inst,seq[0])
    for cur in syms:
        sym=cur['sym']; inst=cur['InstName']
        _check_symattr(cur, msgs)
        nodes=[node_of(c) for c in cur['pincoords']]
        val=fmt_val(cur.get('Value'))
        sl=parse_spiceline(cur.get('SpiceLine'))
        rser=sl.get('rser'); lser=sl.get('lser')
        nm=ename(sym,inst) if sym in TYPELET else inst
        # which SpiceLine keys this branch turns into explicit elements; every
        # key NOT listed here is appended to the card by _card_tail() so the
        # round trip can see it (2026-09-04, hole B1).
        if sym=='res':
            tail=_card_tail(cur,set(),msgs)
            lines.append('%s %s %s %s%s'%(nm,nodes[0],nodes[1],val,tail))
        elif sym=='cap':
            a,b=nodes[0],nodes[1]
            if rser and lser:
                tail=_card_tail(cur,{'rser','lser'},msgs)
                m1=newnode(inst); m2=newnode(inst)
                lines.append('%s %s %s %s%s'%(nm,a,m1,val,tail))
                lines.append('Rser_%s %s %s %s'%(inst,m1,m2,rser))
                lines.append('Lser_%s %s %s %s'%(inst,m2,b,lser))
            elif rser:
                tail=_card_tail(cur,{'rser'},msgs)
                m1=newnode(inst)
                lines.append('%s %s %s %s%s'%(nm,a,m1,val,tail))
                lines.append('Rser_%s %s %s %s'%(inst,m1,b,rser))
            elif lser:
                tail=_card_tail(cur,{'lser'},msgs)
                m1=newnode(inst)
                lines.append('%s %s %s %s%s'%(nm,a,m1,val,tail))
                lines.append('Lser_%s %s %s %s'%(inst,m1,b,lser))
            else:
                tail=_card_tail(cur,set(),msgs)
                lines.append('%s %s %s %s%s'%(nm,a,b,val,tail))
        elif sym in ('ind','ind2'):
            a,b=nodes[0],nodes[1]
            if rser:
                tail=_card_tail(cur,{'rser'},msgs)
                m1=newnode(inst)
                # keep the L element on the DOT terminal (pin A = node1) for K coupling
                lines.append('%s %s %s %s%s'%(nm,a,m1,val,tail))
                lines.append('Rser_%s %s %s %s'%(inst,m1,b,rser))
            else:
                tail=_card_tail(cur,set(),msgs)
                lines.append('%s %s %s %s%s'%(nm,a,b,val,tail))
        elif sym=='diode':
            model=val if val else 'D'
            tail=_card_tail(cur,set(),msgs)
            lines.append('%s %s %s %s%s'%(nm,nodes[0],nodes[1],model,tail))  # anode cathode
        elif sym=='voltage':
            nplus,nminus=nodes[0],nodes[1]
            if rser:
                tail=_card_tail(cur,{'rser'},msgs)
                m1=newnode(inst)
                lines.append('Rser_%s %s %s %s'%(inst,nplus,m1,rser))
                lines.append('%s %s %s %s%s'%(nm,m1,nminus,val,tail))
            else:
                tail=_card_tail(cur,set(),msgs)
                lines.append('%s %s %s %s%s'%(nm,nplus,nminus,val,tail))
        elif sym=='sw':
            model=val if val else 'SW'
            tail=_card_tail(cur,set(),msgs)
            # ngspice: S nd+ nd- nc+ nc- model  ; asy order A B NC+ NC-
            lines.append('%s %s %s %s %s %s%s'%(nm,nodes[0],nodes[1],nodes[2],nodes[3],model,tail))
        elif sym in ('nmos','pmos'):
            # ltsym/nmos.asy, pmos.asy: PIN order D(SpiceOrder 1), G(2), S(3).
            # An InstName starting with X means the symbol stands for a
            # SUBCIRCUIT call (SYMATTR Value = subckt name, SYMATTR SpiceLine =
            # instance parameters) -- that is how net2asc.py draws
            # `X<name> d g s <SUBCKT> p=v ...`.  Anything else becomes a plain
            # ngspice M card with the bulk tied to the source.
            model = val if val else ('NMOS' if sym=='nmos' else 'PMOS')
            extra = (cur.get('SpiceLine') or '').strip()
            if inst[:1].upper()=='X':
                # the WHOLE SpiceLine is the call's instance parameters here,
                # so nothing of it is left over (consumed=None).
                tail=_card_tail(cur,None,msgs)
                parts=[inst,nodes[0],nodes[1],nodes[2],model]
                if extra: parts.append(extra)
                lines.append(' '.join(parts)+tail)
            else:
                # a plain M card: the SpiceLine is instance parameters again
                # (w=, l=, m=, ...) and used to be computed and then thrown
                # away.  Carry it (2026-09-04, hole B1).
                tail=_card_tail(cur,None,msgs)
                mn = inst if inst[:1].upper()=='M' else 'M'+inst
                lines.append('%s %s %s %s %s %s%s%s'
                             %(mn,nodes[0],nodes[1],nodes[2],nodes[2],model,
                               (' '+extra) if extra else '', tail))
        elif sym=='jumper':
            # pure wiring: already shorted via union.  A jumper has nowhere to
            # put a value, so anything attached to it would be lost.
            if msgs is not None and (cur.get('Value') or cur.get('Value2')
                                     or cur.get('SpiceLine')
                                     or cur.get('SpiceLine2')):
                msgs.append('ERROR: %s: a Misc\\jumper symbol carries '
                            'SYMATTR Value/SpiceLine, which this extractor has '
                            'nowhere to put (a jumper emits no element card).  '
                            'Refusing rather than dropping it.' % inst)
        else:
            # text kept byte-identical to the pre-2026-09-04 form on purpose:
            # `tail` is empty unless the symbol carried Value2/SpiceLine, so
            # existing extractions do not move.
            tail=_card_tail(cur,None,msgs)
            lines.append('* UNHANDLED SYMBOL %s (%s): nodes=%s%s'
                         %(inst,sym,nodes,tail))
    return lines

# ---------------- directive handling ----------------
def split_directives(directives):
    params=[]   # (name, expr)
    others=[]   # verbatim non-param cards
    tran=None
    for d in directives:
        low=d.lower()
        if low.startswith('.param'):
            body=d[len('.param'):].strip()
            for tok in body.split():
                if '=' in tok:
                    n,e=tok.split('=',1); params.append((n.strip(),e.strip()))
        elif low.startswith('.tran'):
            tran=d
        else:
            others.append(d)
    return params, others, tran

def topo_params(params):
    names={n for n,_ in params}
    exprmap={}
    order_seen=[]
    for n,e in params:
        exprmap[n]=e
        if n not in order_seen: order_seen.append(n)
    ident=re.compile(r'[A-Za-z_]\w*')
    deps={}
    for n,e in exprmap.items():
        d=set(x for x in ident.findall(e) if x in names and x!=n)
        deps[n]=d
    out=[]; visited={}
    def visit(n,stack):
        if visited.get(n)=='done': return
        if visited.get(n)=='temp':  # cycle -> break
            return
        visited[n]='temp'
        for dep in sorted(deps.get(n,())):
            visit(dep,stack+[n])
        visited[n]='done'; out.append(n)
    for n in order_seen: visit(n,[])
    return [(n,exprmap[n]) for n in out]

def translate_tran(tran):
    # LTspice: .tran <Tstep> <Tstop> <Tstart> <Tmax> [startup]
    # ngspice: .tran <Tstep> <Tstop> <Tstart> <Tmax> [uic]
    p=tran.split()
    fields=p[1:]
    kw=''
    if fields and fields[-1].lower() in ('startup','uic','nodeset'):
        kw=fields[-1].lower(); fields=fields[:-1]
    # fields: tstep tstop [tstart [tmax]]
    tstep=fields[0] if len(fields)>0 else '0'
    tstop=fields[1] if len(fields)>1 else '1'
    tstart=fields[2] if len(fields)>2 else '0'
    tmax=fields[3] if len(fields)>3 else ''
    if tstep in ('0','0s') or float_or(tstep)==0.0:
        tstep = tmax if tmax else '1n'  # ngspice requires tstep>0
    uic = 'uic' if kw in ('startup','uic') else ''
    parts=['.tran',tstep,tstop,tstart]
    if tmax: parts.append(tmax)
    if uic: parts.append(uic)
    return ' '.join(parts), kw

def float_or(x):
    m=re.match(r'^([0-9.eE+\-]+)',x)
    try: return float(m.group(1)) if m else None
    except Exception: return None

# ---------------- convergence-aid defaults ----------------
# These are ngspice numeric knobs, NOT circuit values.  They exist because this
# project's decks are stiff (behavioural switches + body-diode commutations);
# see LTSPICE_CONVERGENCE_FIXES.md.  They are DEFAULTS: a key is emitted only
# when the source .asc does not set it itself, because in ngspice the LAST
# .options wins and an unconditional trailing .options would silently overrule
# a value the schematic author deliberately chose (e.g. llc.asc asks for
# trtol=7; the old unconditional 'trtol=100' changed the reported efficiency).
OPTION_AIDS = (('itl4', '1000'), ('trtol', '100'))

_OPT_CARD = re.compile(r'^\s*\.opt(?:ions|ion)?\b(.*)$', re.IGNORECASE | re.DOTALL)

def option_keys(directives):
    """Set of option keys already set by the deck's own .options/.option cards.

    Handles 'key=value', bare flags ('savecurrents') and stray spaces around
    '=' ('trtol = 7').  Keys are lower-cased (ngspice options are case
    insensitive)."""
    keys = set()
    for d in directives:
        m = _OPT_CARD.match(d)
        if not m:
            continue
        body = re.sub(r'\s*=\s*', '=', m.group(1))
        for tok in body.split():
            k = tok.split('=', 1)[0].strip().lower()
            if k:
                keys.add(k)
    return keys

def convergence_aid_lines(others, mode='auto'):
    """Lines for the convergence-aid block.

    mode='auto'   : emit only the aid keys the .asc does not already set.
    mode='legacy' : pre-2026-08-25 behaviour -- emit all aids unconditionally
                    (they then override the deck's own values; kept only so an
                    old result can be reproduced bit-for-bit).
    mode='off'    : emit nothing but a note."""
    aid = ' '.join('%s=%s' % (k, v) for k, v in OPTION_AIDS)
    if mode == 'off':
        return ['* ngspice numeric convergence aids suppressed (--no-options-aids);',
                '*   only the .asc\'s own .options cards above are in effect.']
    if mode == 'legacy':
        return ['* LEGACY MODE (--legacy-options): the convergence aids below are',
                '*   emitted unconditionally and, because the LAST .options wins in',
                '*   ngspice, they OVERRIDE any value the .asc set for the same key.',
                '.options %s' % aid]
    present = option_keys(others)
    missing = [(k, v) for k, v in OPTION_AIDS if k not in present]
    kept = [k for k, _ in OPTION_AIDS if k in present]
    out = ['* ngspice numeric convergence aids (NOT a circuit change): itl4=1000',
           '*   (per the .asc convergence memo ngspice recipe) and trtol=100 relax',
           '*   LTE/step-control so the stiff behavioural-switch + body-diode',
           '*   commutations do not collapse the timestep.  They are DEFAULTS: in',
           '*   ngspice the LAST .options wins, so a key is emitted here only when',
           "*   the .asc's own .options cards above do not already set it."]
    if not missing:
        out.append('*   the .asc sets every aid key itself (%s); nothing injected.'
                   % ', '.join(kept))
        return out
    if kept:
        out.append('*   set by the .asc, left untouched: %s' % ', '.join(kept))
    out.append('.options %s' % ' '.join('%s=%s' % (k, v) for k, v in missing))
    return out

# ---------------- non-ASCII in emitted cards ----------------
# 2026-09-05 (audit_fable4, hole E1).  `.param η=0.85` was rewritten to
# `.param eta=0.85` on its way into the deck, but a REFERENCE to the same
# parameter inside a device value (`R1 in mid {1k*η}`) was copied through
# untouched.  The emitted deck then defined `eta` and used `η`, and ngspice
# stopped with `Undefined parameter` / `Cannot compute substitute` -- while
# net2asc.py --check reported VERIFY: PASS, because BOTH sides of its
# comparison carry the same untranslated string.  A deck that cannot run is
# not a PASS.
#
# Two characters are translated, and only where the translation is
# unambiguous:
#   * U+03B7 GREEK SMALL LETTER ETA -> `eta`, anywhere.  It can only be part
#     of an identifier; ngspice has no use for it as a suffix.
#   * U+00B5 MICRO SIGN and U+03BC GREEK SMALL LETTER MU -> `u`, but ONLY
#     directly after a digit or a decimal point, i.e. where it is a magnitude
#     suffix (`1µ`), never where it might be an identifier.  Measured on
#     ngspice-41: `1µ` (U+00B5) parses as 1e-6, but `1μ` (U+03BC) parses as
#     **1.0** with only a `warning, can't find model '1μ'` -- a silent factor
#     of a million.  Neither character occurs in this project's 191 .asc
#     files (checked 2026-09-05), so this is a trap that was set, not one
#     that had been sprung.
# Anything else non-ASCII left in a CARD (comment lines are exempt: they
# carry the title and the Japanese notes, and ngspice ignores them) is
# reported as an ERROR rather than translated by guesswork.  net2asc.py
# treats an ERROR: from the extractor as a failed check, so such a deck can
# no longer be handed over with a PASS.
_MU_SUFFIX = re.compile(r'(?<=[0-9.])[\u00b5\u03bc]')


def to_ascii_card(line):
    """Translate the non-ASCII spellings ngspice cannot read.  See above."""
    return _MU_SUFFIX.sub('u', line.replace('\u03b7', 'eta'))


def ascii_card_check(lines, msgs=None):
    """Translate every card in `lines`; ERROR on non-ASCII we will not guess."""
    out = []
    for ln in lines:
        if ln.startswith('*'):          # comment: ngspice never reads it
            out.append(ln); continue
        t = to_ascii_card(ln)
        bad = sorted({c for c in t if ord(c) > 127})
        if bad and msgs is not None:
            msgs.append('ERROR: card carries characters ngspice will not read '
                        'the way LTspice does (%s); refusing to guess a '
                        'translation.  The card is: %s'
                        % (', '.join('U+%04X %r' % (ord(c), c) for c in bad),
                           t.strip()))
        out.append(t)
    return out


def emit(ascfile, libdir, title=None, options_aids='auto', messages=None):
    pins=load_asy(libdir, messages)
    syms, allpins, node_of, find, directives, aliases = parse_asc(ascfile, pins)
    dev=emit_devices(syms, node_of, messages)
    params, others, tran = split_directives(directives)
    params=topo_params(params)

    L=[]
    L.append('* %s'%(title or ('Faithful ngspice deck auto-generated from '+os.path.basename(ascfile))))
    L.append('* generated by asc2ngspice.py from %s'%os.path.abspath(ascfile))
    L.append('* NOTE: LTspice Rser/Lser expanded to explicit series R/L; pi injected;')
    L.append('*       .tran startup -> uic ; params topologically sorted;')
    L.append('*       eta/micro spelled in ASCII (see to_ascii_card).')
    for grp in aliases:
        L.append('* WARNING: these net labels are ELECTRICALLY THE SAME NODE in this')
        L.append('*   schematic (one connected component carries all of them): %s'
                 % ', '.join(grp))
    L.append('')
    L.append('.param pi=3.14159265358979')
    L.append('')
    L.append('* ---- parameters ----')
    for n,e in params:
        L.append('.param %s=%s'%(n,e))   # ascii_card_check() below translates η
    L.append('')
    L.append('* ---- models / options / coupling ----')
    for d in others:
        L.append(d)
    L.extend(convergence_aid_lines(others, options_aids))
    L.append('')
    L.append('* ---- devices ----')
    L.extend(dev)
    L.append('')
    if tran:
        tt,kw=translate_tran(tran)
        L.append('* original LTspice: %s   (startup->uic)'%tran)
        L.append(tt)
    L.append('')
    L.append('.end')
    L = ascii_card_check(L, messages)
    return '\n'.join(L)+'\n'

if __name__=='__main__':
    # Resolved relative to THIS file so the tool works wherever it is unpacked.
    libdir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ltsym')
    args=sys.argv[1:]
    out=None
    mode='auto'
    if '--legacy-options' in args:
        args.remove('--legacy-options'); mode='legacy'
    if '--no-options-aids' in args:
        args.remove('--no-options-aids'); mode='off'
    if '-o' in args:
        i=args.index('-o'); out=args[i+1]; del args[i:i+2]
    rc=0
    for asc in args:
        msgs=[]
        deck=emit(asc, libdir, options_aids=mode, messages=msgs)
        for m in msgs:
            sys.stderr.write('%s\n'%m)   # stderr: stdout may be the deck itself
            if m.startswith('ERROR:'):
                rc=1
        if out:
            open(out,'w').write(deck); print('wrote',out)
        else:
            sys.stdout.write(deck)
    sys.exit(rc)

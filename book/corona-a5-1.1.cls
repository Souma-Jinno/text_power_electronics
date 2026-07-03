%%
%%
%% This is file `corona-a5.cls',
%% A5 13QX35wx28L(25H)
%% 左右中央、地 17mm
%% 天 版面まで21mm, 柱上まで14mm
%%
%% 
%% 
%% 
\NeedsTeXFormat{pLaTeX2e}
\ProvidesClass{corona-a5}
%  [2005/12/01 v1.0
%  [2006/11/09 v1.0
  [2007/10/31 v1.0
pLaTeX class ALL Rights reserved
Copyright SANBI Co., Ltd. for CORONA PUBLISHING CO., Ltd.]



\edef\VerTYPEOUT{\csname ver@\@currname.\@currext\endcsname}
\AtEndDocument{\typeout{>>>>>\VerTYPEOUT<<<<<}}

%\usepackage[dvips]{graphicx}%%%!!![dvips],[dviout]はクラスオプションにしてく
%		     %%%ださい
%%%% class options %%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Color プログラム環境で使用
\RequirePackage[usenames]{color}      %%%%colorパッケージを読み込む
\RequirePackage{keyval}%%%
\newif\if@Proof \@Prooffalse%★
\DeclareOption{Proof}{\@Prooftrue}

%\DeclareOption{Prooffalse}{\@Prooffalse}

\newif\if@Nopsfont \@Nopsfontfalse%★
\DeclareOption{Nopsfont}{\@Nopsfonttrue}


\newif\if@MASUME \@MASUMEfalse%★
\DeclareOption{MASUME}{\@MASUMEtrue}



\ExecuteOptions{Prooffalse,MASUMEfalse}

\ProcessOptions




\definecolor{AMIxx}{cmyk}{0, 0, 0, 0.2}

%%% MASUME のカラー
\definecolor{REYoutI}{cmyk}{0.5,0,0.75,0.20}


%%%%%%%%%%%%%%%%% These are borrowed style files %%%%%%%%%%%
%%% from 藤田眞作 化学者・生化学者のためのLaTeX
\def\pushtowall{\relax\leavevmode
\ifmmode\def\next{\mathpalette\mathpushw@ll}
\else\let\next\makepushw@ll \fi \next}
\def\finpushw@ll{\wd0=0pt \box0}
\def\makepushw@ll#1{\setbox0=\hbox{#1}\finpushw@ll}
\def\mathpushw@ll#1#2{\setbox0=\hbox{$\m@th#1{#2}$}\finpushw@ll}
%%%% 

%%%%% from indent.sty
% Newsgroups: comp.text.tex
% From: cameron@symcom.math.uiuc.edu (Cameron Smith)

\newenvironment{indentation}[2]%
{%
  \par
  \setlength{\leftmargin}{#1}%
  \setlength{\rightmargin}{#2}%
  \advance\linewidth -\leftmargin
  \advance\linewidth -\rightmargin
  \advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
}%
{\par}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%% from here.sty
%%%  @LaTeX-style-file{e
%%%     filename        = "here.sty",
%%%     version         = "1.01",
%%%     date            = "12 June 1992",
%%%     time            = "15:26:24 BST",
%%%     author          = "David Carlisle",
%%%     here.sty
%%% ====================================================================
%\ifx\@Hxfloat\@Hundef\else\expandafter\endinput\fi
%\let\@Hxfloat\@xfloat
%\def\@xfloat#1[{\@ifnextchar{H}{\@HHfloat{#1}[}{\@Hxfloat{#1}[}}
%\def\@HHfloat#1[H]{%
%\expandafter\let\csname end#1\endcsname\end@Hfloat
%\vskip\intextsep\vbox\bgroup\let\center=\Center\def\@captype{#1}\parindent\z@
%\ignorespaces}
%\def\end@Hfloat{\egroup\vskip \intextsep}




%% \endinput
%% 
%% End of file `here.sty'.
%%%%%%%%%%%%%%%%%%%%%%%% boorowed %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%% コラムが入るので、そのマクロ関係 %%%%%%
%%%%%%  From eclbkbox.sty by Hideki Isozaki, 1992 % Date: Oct. 30, 1992 %%
%%%%% 
%%%%% 
\newbox\COFFEEbk@bxb
\newbox\COFFEEbk@bxa
\newif\if@COFFEEbkcont 
\newif\ifCOFFEEbkcount
\newcount\COFFEEbk@lcnt


\def\COFFEEbreakbox{\fboxsep=3.25mm\fboxrule=.25mm\setbox\COFFEEbk@bxb\vbox\bgroup
\clubpenalty \z@
\advance\linewidth -2\fboxrule
\advance\linewidth -2\fboxsep
\hsize\linewidth\@parboxrestore}

% \@tempdimb: amount of vertical skip 
% between the first line (\COFFEEbk@bxa) and the rest (\COFFEEbk@bxb)
\def\COFFEEbk@split{%
\@tempdimb\ht\COFFEEbk@bxb
\setbox\COFFEEbk@bxa\vsplit\COFFEEbk@bxb to\z@
\setbox\COFFEEbk@bxa\vbox{\unvbox\COFFEEbk@bxa}%
\setbox\@tempboxa\vbox{\copy\COFFEEbk@bxa\copy\COFFEEbk@bxb}%
\advance\@tempdimb-\ht\@tempboxa}

% \@tempdima: height of the first line (\COFFEEbk@bxa) + fboxsep
\def\COFFEEbk@addfsepht{%
     \setbox\COFFEEbk@bxa\vbox{\vskip\fboxsep\box\COFFEEbk@bxa}}

\def\COFFEEbk@addskipht{%
     \setbox\COFFEEbk@bxa\vbox{\vskip\@tempdimb\box\COFFEEbk@bxa}}

% \@tempdima: depth of the first line (\COFFEEbk@bxa) + fboxsep
\def\COFFEEbk@addfsepdp{%
     \@tempdima\dp\COFFEEbk@bxa
     \advance\@tempdima\fboxsep
     \dp\COFFEEbk@bxa\@tempdima}

% \@tempdima: depth of the first line (\COFFEEbk@bxa) + vertical skip
\def\COFFEEbk@addskipdp{%
     \@tempdima\dp\COFFEEbk@bxa
     \advance\@tempdima\@tempdimb
     \dp\COFFEEbk@bxa\@tempdima}

\def\COFFEEbk@line{%
    \hbox to \linewidth{\ifCOFFEEbkcount\smash{\llap{\the\COFFEEbk@lcnt\ }}\fi
    \vrule \@width\fboxrule\hskip\fboxsep
    \box\COFFEEbk@bxa\hfil
    \hskip\fboxsep\vrule \@width\fboxrule}}

\def\Hrulefill{\leavevmode\leaders\hrule\@height.25mm\hfill\kern\z@}
\def\Hrulefillxmm{\leavevmode\leaders\hrule\@height.25mm width 10mm\hfill\kern\z@}
\def\COFFEEhrulefill{\leavevmode\leaders\Hrule\hfill\kern\z@\@height\fboxrule}


\newskip\endCOFFEEskip
\setlength{\endCOFFEEskip}{10.5H}

\def\endCOFFEEbreakbox{\egroup
\ifhmode\par\fi{\noindent\COFFEEbk@lcnt\@ne \clubpenalty\@M
\@COFFEEbkconttrue\baselineskip\z@\lineskiplimit\z@
\lineskip\z@\vfuzz\maxdimen
\COFFEEbk@split\ifdim\wd\COFFEEbk@bxa=\z@\ifdim\ht\COFFEEbk@bxa=\z@\COFFEEbk@split\fi\fi
\COFFEEbk@addfsepht\COFFEEbk@addskipdp
\ifvoid\COFFEEbk@bxb      % Only one line
%\setlength{\endCOFFEEskip}{1H}
\def\COFFEEbk@fstln{\COFFEEbk@addfsepdp%
\vbox{\hbox to\hsize{\hbox to10mm{\Hrulefillxmm}\smash{\raisebox{-.75mm}{\fboxsep1mm\fboxrule.12mm\fbox{\bfseries コーヒーブレイク}}}\Hrulefill}%\@height\fboxrule 
\COFFEEbk@line\hrule\@height\fboxrule}}%
\else               % More than one line
%\def\COFFEEbk@fstln{\vbox{\hrule\@height\fboxrule\COFFEEbk@line}\hfil
\def\COFFEEbk@fstln{\vbox{
\hbox to\hsize{\hbox to10mm{\Hrulefillxmm}\smash{\raisebox{-.75mm}{\fboxsep1mm\fboxrule.12mm\fbox{\bfseries コーヒーブレイク}}}\Hrulefill}
%\hrule\@height\fboxrule
\COFFEEbk@line
}\hfil
%
%
\advance\COFFEEbk@lcnt\@ne
\loop 
 \COFFEEbk@split\COFFEEbk@addskipdp\leavevmode
\ifvoid\COFFEEbk@bxb      % The last line
 \@COFFEEbkcontfalse\COFFEEbk@addfsepdp
 \vtop{\COFFEEbk@line\hrule\@height\fboxrule}\par%\endCOFFEEskip% 複数
\else               % 2,...,(n-1)
 \COFFEEbk@line 
\fi
 \hfil\advance\COFFEEbk@lcnt\@ne
\if@COFFEEbkcont\repeat}%
\fi
\leavevmode\COFFEEbk@fstln\par}}

\COFFEEbkcountfalse





%%%%%%%%%%%%%%%%%%%%%%% end input %%%%%%%%%%%%%%%%%%%%%
%%% コーヒーブレークというコラム

%%
\newcounter{COFFcount}
\renewcommand{\theCOFFcount}{★\@arabic\c@COFFcount ★}


\newcommand{\be}{\begin{equation}}
\newcommand{\ee}{\end{equation}}


\newenvironment{COLUMN}{%\let\figure\COFFfigure%
%\refstepcounter{COFFequation}%
\renewenvironment{figure}{\begin{COFFfigure}}{\end{COFFfigure}}%
\renewenvironment{table}{\begin{COFFtable}}{\end{COFFtable}}%
%\let\equation\COFFequation
%%\renewenvironment{equation}{\begin{COFFequation}}{\end{COFFequation}}%
%%\renewenvironment{eqnarray}{\begin{COFFeqnarray}}{\end{COFFeqnarray}}%
%\let\table\COFFtable%
%%\renewcommand{\be}{\begin{COFFequation}}
%%\renewcommand{\ee}{\end{COFFequation}}
%\let\@eqnnum\@COFFeqnnum
%
\let\equation\COFFequation
\let\endequation\endCOFFequation
\let\eqnarray\COFFeqnarray
\let\endeqnarray\endCOFFeqnarray
\let\nonumber\COFFnonumber
\@namedef{eqnarray*}{\def\@COFFeqncr{\COFFnonumber\@COFFseqncr}\COFFeqnarray}
\@namedef{endeqnarray*}{\COFFnonumber\endCOFFeqnarray}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewenvironment{subequations}{%
\renewcommand{\theCOFFequation}{%
\ifnum\c@chapter>\z@\relax\fi \@arabic\c@COFFequation}
  \refstepcounter{COFFequation}%
  \protected@edef\theparentequation{\theCOFFequation}%
  \setcounter{parentequation}{\value{COFFequation}}%
  \setcounter{COFFequation}{0}%
  \def\theCOFFequation{(\theparentequation\alph{COFFequation})}%
  \ignorespaces
}{%
  \setcounter{COFFequation}{\value{parentequation}}%
  \ignorespacesafterend
}
%%%%
%}
%}
%% (  )は \theequationにとりあえず入れたが、後で、検証
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%\let\theequation\theCOFFequation
%\let\be\beCOFF
%\let\ee\eeCOFF
%\let\Msubequations\MCOFFsubequations
%\let\tagform@\COFFtagform@
%\def\fnum@figure{\theCOFFfigure}\setcounter{COFFfigure}{0}\refstepcounter{COFFcount}%
%\refstepcounter{COFFfigure}\let\thefigure\theCOFFfigure
\vskip24\h\begin{COFFEEbreakbox}%\theCOFFcount%
\small\parindent=1zw\addvspace{1.5mm}}{%
%\end{COFFEEbreakbox}\vskip10.5\h}
\end{COFFEEbreakbox}%\vskip\endCOFFEEskip
}
%\ifvoid\COFFEEbk@bxb
%%%%%%%%%%%%%%%%%%%%%%%%% eclbkbox %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%








%%% 均等に関する
\newcommand{\kintou}[2]{%
\leavevmode
\hbox to #1{%
\kanjiskip=0pt plus 1fill minus 1fill
\xkanjiskip=\kanjiskip
#2%
}}



%% 7字ドリ
\long\def\SEVENjidori#1{%
\settowidth{\@tempdima}{#1}%
\@SEVENjidori{\@tempdima}{#1}}

\long\def\@SEVENjidori#1#2{%
%\ifdim#1<1.2zw \protect\kintou{7zw}{#2}\else%
%\ifdim#1<2.4zw
%     \protect\kintou{3zw}{#2}\else%
%\ifdim#1<3.4zw
%    \protect\kintou{5zw}{#2}\else%
%\ifdim#1<4.4zw
%     \protect\kintou{7zw}{#2}\else%
%\ifdim#1<5.4zw
%     \protect\kintou{7zw}{#2}\else%
%\ifdim#1<6.4zw
%     \protect\kintou{7zw}{#2}\else%
\ifdim#1<7.4zw
     \protect\kintou{7zw}{#2}\else%
%\ifdim#1<8.4zw
%     \protect\SEVENjidori{7zw}{#2}\else%
%\ifdim#1<9.4zw
%     \protect\SEVENjidori{7zw}{#2}\else%
%\ifdim#1<10.4zw
%     \protect\SEVENjidori{7zw}{#2}\else%
%\ifdim#1<11.4zw
%     \protect\SEVENjidori{7zw}{#2}\else%
%\hbox
%{\kanjiskip=0zw plus.4pt minus.5pt#2}%
{%\kanjiskip=0pt plus 1fill minus 1fill
%\xkanjiskip=\kanjiskip
#2}%
\fi%\fi%\fi\fi\fi\fi\fi%\fi\fi\fi\fi%
}






%% 5字ドリ \subsubsection, \paragraph
\long\def\FIVEjidori#1{%
\settowidth{\@tempdima}{#1}%
\@FIVEjidori{\@tempdima}{#1}}

\long\def\@FIVEjidori#1#2{%
\ifdim#1<5.4zw
     \protect\kintou{5zw}{#2}\else%
{#2}%
\fi%
}









%% 11字ドリ
\long\def\ELEVENjidori#1{%
\settowidth{\@tempdima}{#1}%
\@ELEVENjidori{\@tempdima}{#1}}

\long\def\@ELEVENjidori#1#2{%
\ifdim#1<11.4zw
     \protect\kintou{11zw}{#2}\else%
#2%
\fi%
}








%% 2字以下=5字どり / 7字以下3以上 7字ドリ
\def\HASIRAkintou#1{%
\settowidth{\@tempdima}{#1}%
\@HASIRAkintou{\@tempdima}{#1}}

\def\@HASIRAkintou#1#2{%
\ifdim#1<1.2zw \protect\kintou{9zw}{#2}\else%
\ifdim#1<2.4zw
     \protect\kintou{9zw}{#2}\else%
\ifdim#1<3.4zw
     \protect\kintou{9zw}{#2}\else%
\ifdim#1<4.4zw
     \protect\kintou{9zw}{#2}\else%
\ifdim#1<5.4zw
     \protect\kintou{9zw}{#2}\else%
\ifdim#1<6.4zw
     \protect\kintou{9zw}{#2}\else%
\ifdim#1<7.4zw
     \protect\kintou{9zw}{#2}\else%
\ifdim#1<8.4zw
     \protect\kintou{9zw}{#2}\else%
\ifdim#1<9.4zw
     \protect\kintou{9zw}{#2}\else%
\ifdim#1<10.4zw
     \protect\kintou{9zw}{#2}\else%
\ifdim#1<11.4zw
     \protect\kintou{9zw}{#2}\else%
%\hbox
{\kanjiskip=0zw plus.4pt minus.5pt#2}%
\fi\fi\fi\fi\fi\fi\fi\fi\fi\fi\fi
}








%% 目次用の7字ドリ
\long\def\mokuSEVENjidori#1{%
\settowidth{\@tempdima}{#1}%
\@mokuSEVENjidori{\@tempdima}{#1}}

\long\def\@mokuSEVENjidori#1#2{%
%\ifdim#1<1.2zw \protect\kintou{7zw}{#2}\else%
%\ifdim#1<2.4zw
%     \protect\kintou{3zw}{#2}\else%
%\ifdim#1<3.4zw
%    \protect\kintou{5zw}{#2}\else%
%\ifdim#1<4.4zw
%     \protect\kintou{7zw}{#2}\else%
%\ifdim#1<5.4zw
%     \protect\kintou{7zw}{#2}\else%
%\ifdim#1<6.4zw
%     \protect\kintou{7zw}{#2}\else%
\ifdim#1<7.4zw
     \protect\kintou{7zw}{#2}\else%
%\ifdim#1<8.4zw
%     \protect\SEVENjidori{7zw}{#2}\else%
%\ifdim#1<9.4zw
%     \protect\SEVENjidori{7zw}{#2}\else%
%\ifdim#1<10.4zw
%     \protect\SEVENjidori{7zw}{#2}\else%
%\ifdim#1<11.4zw
%     \protect\SEVENjidori{7zw}{#2}\else%
%\hbox
%{\kanjiskip=0zw plus.4pt minus.5pt#2}%
{%\kanjiskip=0pt plus 1fill minus 1fill
%\xkanjiskip=\kanjiskip
#2}%
\fi%\fi%\fi\fi\fi\fi\fi%\fi\fi\fi\fi%
}













%% 全角よりはみ出るルビの長さによる隣の文字との空き、と行間空きを防ぐ

\newcommand{\ruby}[2]{%
\leavevmode
\setbox1=\hbox{#1}%
\setbox3=\hbox{\fontsize{7\JQ}{9H}\selectfont
#2}%
\ifdim\wd1>\wd3 \dimen1=\wd1 \else \dimen1=\wd3 \fi
\hbox{%
\kanjiskip=0pt plus 2fil
\xkanjiskip=0pt plus 2fil
\vbox{\hbox to \dimen1{\fontsize{7\JQ}{9H}\selectfont \hss\unhbox3\hss}%
\nointerlineskip
\hbox to \dimen1{\hfil\unhbox1\hfil}}}}




%%% center環境の調整
\def\Center{\topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
 \trivlist \centering\item\relax}
\def\endCenter{\endtrivlist}


%%%% parameter %%%%%%%%%
\unitlength=1mm
\predisplaypenalty=0

%%%%%%%%%%%%%%%%%%%%%%%%

%%% 中細罫 表組みの天
\def\Hline{\noalign{\hrule height .25mm}}


\newcounter{@paper}
\newif\if@landscape \@landscapefalse
\newcommand{\@ptsize}{}
\newif\if@restonecol
\newif\if@titlepage
\@titlepagetrue
\newif\if@openright
\newif\if@mainmatter \@mainmattertrue
\hour\time \divide\hour by 60\relax
\@tempcnta\hour \multiply\@tempcnta 60\relax
\minute\time \advance\minute-\@tempcnta
\newif\if@stysize \@stysizefalse
\newif\if@enablejfam \@enablejfamtrue
\DeclareOption{a4paper}{\setcounter{@paper}{1}%
  \setlength\paperheight {297mm}%
  \setlength\paperwidth  {210mm}}
\DeclareOption{a5paper}{\setcounter{@paper}{2}%
  \setlength\paperheight {210mm}
  \setlength\paperwidth  {148mm}}
\DeclareOption{b4paper}{\setcounter{@paper}{3}%
  \setlength\paperheight {364mm}
  \setlength\paperwidth  {257mm}}
\DeclareOption{b5paper}{\setcounter{@paper}{4}%
  \setlength\paperheight {257mm}
  \setlength\paperwidth  {182mm}}
\DeclareOption{a4j}{\setcounter{@paper}{1}\@stysizetrue
  \setlength\paperheight {297mm}%
  \setlength\paperwidth  {210mm}}
\DeclareOption{a5j}{\setcounter{@paper}{2}\@stysizetrue
  \setlength\paperheight {210mm}
  \setlength\paperwidth  {148mm}}
\DeclareOption{b4j}{\setcounter{@paper}{3}\@stysizetrue
  \setlength\paperheight {364mm}
  \setlength\paperwidth  {257mm}}
\DeclareOption{b5j}{\setcounter{@paper}{4}\@stysizetrue
  \setlength\paperheight {257mm}
  \setlength\paperwidth  {182mm}}
\DeclareOption{a4p}{\setcounter{@paper}{1}\@stysizetrue
  \setlength\paperheight {297mm}%
  \setlength\paperwidth  {210mm}}
\DeclareOption{a5p}{\setcounter{@paper}{2}\@stysizetrue
  \setlength\paperheight {210mm}
  \setlength\paperwidth  {148mm}}
\DeclareOption{b4p}{\setcounter{@paper}{3}\@stysizetrue
  \setlength\paperheight {364mm}
  \setlength\paperwidth  {257mm}}
\DeclareOption{b5p}{\setcounter{@paper}{4}\@stysizetrue
  \setlength\paperheight {257mm}
  \setlength\paperwidth  {182mm}}
\if@compatibility
  \renewcommand{\@ptsize}{0}
\else
  \DeclareOption{10pt}{\renewcommand{\@ptsize}{0}}
\fi
\DeclareOption{11pt}{\renewcommand{\@ptsize}{1}}
\DeclareOption{12pt}{\renewcommand{\@ptsize}{2}}
\DeclareOption{landscape}{\@landscapetrue
  \setlength\@tempdima{\paperheight}%
  \setlength\paperheight{\paperwidth}%
  \setlength\paperwidth{\@tempdima}}
\DeclareOption{tombow}{%
  \tombowtrue \tombowdatetrue
  \setlength{\@tombowwidth}{.1\p@}%
  \@bannertoken{%
     \jobname\space:\space\number\year/\number\month/\number\day
      (\number\hour:\number\minute)}
  \maketombowbox}
\DeclareOption{tombo}{%
  \tombowtrue \tombowdatefalse
  \setlength{\@tombowwidth}{.1\p@}%
  \maketombowbox}
\DeclareOption{mentuke}{%
  \tombowtrue \tombowdatefalse
  \setlength{\@tombowwidth}{\z@}%
  \maketombowbox}
\DeclareOption{tate}{%
  \AtBeginDocument{\tate\message{《縦組モード》}%
                   \adjustbaseline}%
}
\DeclareOption{oneside}{\@twosidefalse}
\DeclareOption{twoside}{\@twosidetrue}
\DeclareOption{onecolumn}{\@twocolumnfalse}
\DeclareOption{twocolumn}{\@twocolumntrue}
\DeclareOption{titlepage}{\@titlepagetrue}
\DeclareOption{notitlepage}{\@titlepagefalse}
\if@compatibility
\@openrighttrue
\else
\DeclareOption{openright}{\@openrighttrue}
\DeclareOption{openany}{\@openrightfalse}
\fi
\DeclareOption{leqno}{\input{leqno.clo}}
\DeclareOption{fleqn}{\input{fleqn.clo}}
\DeclareOption{openbib}{%
  \AtEndOfPackage{%
   \renewcommand\@openbib@code{%
      \advance\leftmargin\bibindent
      \itemindent -\bibindent
      \listparindent \itemindent
      \parsep \z@
      }%
   \renewcommand\newblock{\par}}}
\if@compatibility
\else
  \DeclareOption{disablejfam}{\@enablejfamfalse}
\fi
\DeclareOption{draft}{\setlength\overfullrule{5pt}}
\DeclareOption{final}{\setlength\overfullrule{0pt}}
\ExecuteOptions{a4paper,10pt,twoside,onecolumn,final,openright}
\ProcessOptions\relax
%%%%%\input{jbk1\@ptsize.clo}


\newdimen\h
\h=0.25mm
\newdimen\JQ % for SK fonts
\JQ=0.7392507pt
\newdimen\Q % for SE fonts
\Q=0.71144pt
\newdimen\@bs
\@bs=25\h





\expandafter\let\csname JY1/mc/m/n/10\endcsname\relax
\expandafter\let\csname JY1/gt/m/n/10\endcsname\relax




\DeclareFontShape{JY1}{mc}{m}{n}{<6> jis
 <5> s * [1.1828] jis % 8級 tiny
 <7> s * [1.056072] jis      % 10級  scriptsize
 <8> s * [1.01647] jis      % 11級  footnotesize
 <9> s * [0.9856] jis      % 12級  small
 <10> s * [0.961] jis      % 13級  normalsize
 <10.95> s * [1.075303] jis % 16級  large
 <12> s * [1.108906] jis    % 18級  Large
 <14.4> s * [1.026765] jis  % 20級  LARGE
 <17.28> s * [1.026765] jis % 24級  huge
 <20.74> s * [0.998051] jis % 28級  Huge
 <24.88> s * [0.9508] jis  % 32級  HUGE
 <-> jis
 }{}



%\DeclareFontShape{JY1}{mc}{m}{n}{
% <-> s * [0.961] jis
% }{}


 \DeclareFontShape{JY1}{mc}{bx}{n}{<6> jisg
 <5> s * [1.1828] jisg% 8級 tiny
 <7> s * [1.056072] jisg      % 10級  scriptsize
 <8> s * [1.01647] jisg      % 11級  footnotesize
 <9> s * [0.9856] jisg      % 12級  small
 <10> s * [0.961] jisg      % 13級  normalsize
 <10.95> s * [1.075303] jisg % 16級  large
 <12> s * [1.108906] jisg    % 18級  Large
 <14.4> s * [1.026765] jisg  % 20級  LARGE
 <17.28> s * [1.026765] jisg % 24級  huge
 <20.74> s * [0.998051] jisg % 28級  Huge
 <24.88> s * [0.9508] jisg  % 32級  HUGE
 <-> jisg%%%min10
 }{}





% \DeclareFontShape{JY1}{mc}{m}{n}{<-> s * jis}{}
% \DeclareFontShape{JY1}{gt}{m}{n}{<-> s * jisg}{}

%\DeclarePreloadSizes{JY1}{mc}{m}{n}
%  {5,6,7,8,9,10,10.95,12,14.4,17.28,20.74,24.88}
%\DeclarePreloadSizes{JY1}{gt}{m}{n}
%  {5,6,7,8,9,10,10.95,12,14.4,17.28,20.74,24.88}




%% JY1 it
\DeclareFontShape{JY1}{mc}{m}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JY1}{mc}{bx}{it}{<->ssub*gt/m/n}{}
\DeclareFontShape{JY1}{gt}{m}{it}{<->ssub*gt/m/n}{}
\DeclareFontShape{JY1}{gt}{bx}{it}{<->ssub*gt/m/n}{}
%%
\DeclareFontShape{JY1}{mc}{b}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JY1}{mc}{eb}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JY1}{gt}{b}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JY1}{gt}{eb}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JY1}{gt}{ub}{it}{<->ssub*mc/m/n}{}
%% JT1 it
\DeclareFontShape{JT1}{mc}{m}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JT1}{mc}{bx}{it}{<->ssub*gt/m/n}{}
\DeclareFontShape{JT1}{gt}{m}{it}{<->ssub*gt/m/n}{}
\DeclareFontShape{JT1}{gt}{bx}{it}{<->ssub*gt/m/n}{}
%%
\DeclareFontShape{JT1}{mc}{b}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JT1}{mc}{eb}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JT1}{gt}{b}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JT1}{gt}{eb}{it}{<->ssub*mc/m/n}{}
\DeclareFontShape{JT1}{gt}{ub}{it}{<->ssub*mc/m/n}{}
%% sc
\DeclareFontShape{JY1}{mc}{m}{sc}{<->ssub*mc/m/n}{}
\DeclareFontShape{JT1}{mc}{m}{sc}{<->ssub*mc/m/n}{}
%% n
\DeclareFontShape{JY1}{gt}{b}{n}{<->ssub*gt/m/n}{}
\DeclareFontShape{JT1}{gt}{b}{n}{<->ssub*gt/m/n}{}
%% sl
\DeclareFontShape{JY1}{mc}{bx}{sl}{<->ssub*gt/m/n}{}
\DeclareFontShape{JT1}{mc}{bx}{sl}{<->ssub*gt/m/n}{}
\DeclareFontShape{JY1}{mc}{m}{sl}{<->ssub*gt/m/n}{}
\DeclareFontShape{JT1}{mc}{m}{sl}{<->ssub*gt/m/n}{}




\renewcommand{\normalsize}{%
    \@setfontsize\normalsize\@xpt{25H}%
  \abovedisplayskip 10\p@ \@plus2\p@ \@minus5\p@
  \abovedisplayshortskip \z@ \@plus3\p@
  \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
   \belowdisplayskip \abovedisplayskip
   \let\@listi\@listI}
\normalsize
\setbox0\hbox{\char\euc"A1A1}%
\setlength\Cht{\ht0}
\setlength\Cdp{\dp0}
\setlength\Cwd{\wd0}
\setlength\Cvs{\baselineskip}
\setlength\Chs{\wd0}

\newcommand{\small}{%
  \@setfontsize\small\@ixpt{20H}%
  \abovedisplayskip 8.5\p@ \@plus3\p@ \@minus4\p@
  \abovedisplayshortskip \z@ \@plus2\p@
  \belowdisplayshortskip 4\p@ \@plus2\p@ \@minus2\p@
  \def\@listi{\leftmargin\leftmargini
              \topsep 4\p@ \@plus2\p@ \@minus2\p@
              \parsep 2\p@ \@plus\p@ \@minus\p@%\def\@eqnnum{{\normalfont \normalcolor ({\theequation})\quad}}
%\def\tagform@#1{\maketag@@@{(\ignorespaces#1\unskip\@@italiccorr)\quad}
              \itemsep \parsep
}%
  \belowdisplayskip \abovedisplayskip
}

\newcommand{\footnotesize}{%
  \@setfontsize\footnotesize\@viiipt{15H}%
  \abovedisplayskip 6\p@ \@plus2\p@ \@minus4\p@
  \abovedisplayshortskip \z@ \@plus\p@
  \belowdisplayshortskip 3\p@ \@plus\p@ \@minus2\p@
  \def\@listi{\leftmargin\leftmargini
              \topsep 3\p@ \@plus\p@ \@minus\p@
              \parsep 2\p@ \@plus\p@ \@minus\p@
              \itemsep \parsep}%
  \belowdisplayskip \abovedisplayskip}

%\newcommand{\scriptsize}{\@setfontsize\scriptsize\@viipt\@viiipt}
\newcommand{\scriptsize}{\@setfontsize\scriptsize\@viipt{14H}}

%\newcommand{\tiny}{\@setfontsize\tiny\@vpt\@vipt}
\newcommand{\tiny}{\@setfontsize\tiny\@vpt{10H}}

%\newcommand{\large}{\@setfontsize\large\@xipt{28H}}
\newcommand{\large}{\@setfontsize\large{16\JQ}{28H}}
%\DeclareRobustCommand*\large{%
%   \@setfontsize\large{16Q}{18Q}%\defaultbaselineskip
%   \set@xkanjiskip
%}
\newcommand{\Large}{\@setfontsize\Large\@xiipt{30H}}
\newcommand{\LARGE}{\@setfontsize\LARGE\@xivpt{36H}}
\newcommand{\huge}{\@setfontsize\huge\@xviipt{40H}}
\newcommand{\Huge}{\@setfontsize\Huge\@xxpt{44H}}
\newcommand{\HUGE}{\@setfontsize\HUGE\@xxvpt{33}}
\setlength\headheight{12\p@}
\setlength\headsep{4.5mm}
%\newdimen\ASCIIdimen
%\setbox\ASCIIdimen=\hbox{(}
%\newdimen\ASCIIdimenHOSEI
%\ASCIIdimenHOSEI=\ASCIIdimen\advance \ASCIIdimen by -1\Cht
\setlength\topskip{1\Cht}\advance \topskip by 0.0274pt
%\addtolength{\topskip}{-0.0274pt}}% 


\setlength\footskip{.35in}
\if@compatibility
  \setlength\maxdepth{4\p@}
\else
  \setlength\maxdepth{.5\topskip}
\fi
\if@compatibility
  \if@stysize
    \ifnum\c@@paper=2 % A5
      \if@landscape
        \setlength\textwidth{47\Cwd}
      \else
        \setlength\textwidth{28\Cwd}
      \fi
    \else\ifnum\c@@paper=3 % B4
      \if@landscape
        \setlength\textwidth{75\Cwd}
      \else
        \setlength\textwidth{60\Cwd}
      \fi
    \else\ifnum\c@@paper=4 % B5
      \if@landscape
        \setlength\textwidth{60\Cwd}
      \else
        \setlength\textwidth{37\Cwd}
      \fi
    \else % A4 ant other
      \if@landscape
        \setlength\textwidth{73\Cwd}
      \else
        \setlength\textwidth{47\Cwd}
      \fi
    \fi\fi\fi
  \else
    \if@twocolumn
      \setlength\textwidth{52\Cwd}
    \else
      \setlength\textwidth{4.3in}
    \fi
  \fi
\else
  \if@stysize
    \if@twocolumn
      \setlength\textwidth{.8\paperwidth}
    \else
      \setlength\textwidth{.7\paperwidth}
    \fi
  \else
    \setlength\@tempdima{\paperwidth}
    \addtolength\@tempdima{-2in}
    \setlength\@tempdimb{327\p@}
    \if@twocolumn
      \ifdim\@tempdima>2\@tempdimb\relax
        \setlength\textwidth{2\@tempdimb}
      \else
        \setlength\textwidth{\@tempdima}
      \fi
    \else
      \ifdim\@tempdima>\@tempdimb\relax
        \setlength\textwidth{\@tempdimb}
      \else
        \setlength\textwidth{\@tempdima}
      \fi
    \fi
  \fi
\fi
\@settopoint\textwidth
\if@compatibility
  \if@stysize
    \ifnum\c@@paper=2 % A5
      \if@landscape
        \setlength\textheight{17\Cvs}
      \else
        \setlength\textheight{28\Cvs}
      \fi
    \else\ifnum\c@@paper=3 % B4
      \if@landscape
        \setlength\textheight{38\Cvs}
      \else
        \setlength\textheight{57\Cvs}
      \fi
    \else\ifnum\c@@paper=4 % B5
      \if@landscape
        \setlength\textheight{22\Cvs}
      \else
        \setlength\textheight{35\Cvs}
      \fi
    \else % A4 and other
      \if@landscape
        \setlength\textheight{27\Cvs}
      \else
        \setlength\textheight{43\Cvs}
      \fi
    \fi\fi\fi
    \addtolength\textheight{\topskip}
    \addtolength\textheight{\baselineskip}
  \else
  \setlength\textheight{554\p@}
  \fi
\else
  \if@stysize
    \setlength\textheight{.70\paperheight}
  \else
    \setlength\@tempdima{\paperheight}
    \addtolength\@tempdima{-2in}
    \addtolength\@tempdima{-1.5in}
    \divide\@tempdima\baselineskip
    \@tempcnta\@tempdima
    \setlength\textheight{\@tempcnta\baselineskip}
  \fi
\fi
\addtolength\textheight{\topskip}
\@settopoint\textheight
\if@compatibility
  \if@stysize
    \setlength\topmargin{-.3in}
  \else
    \setlength\topmargin{.75in}
  \fi
\else
  \setlength\topmargin{\paperheight}
  \addtolength\topmargin{-\headheight}
  \addtolength\topmargin{-\headsep}
  \addtolength\topmargin{-\textheight}
  \addtolength\topmargin{-\footskip}
  \if@stysize
    \ifnum\c@@paper=2 % A5
      \addtolength\topmargin{-1.3in}
    \else
      \addtolength\topmargin{-2.0in}
    \fi
  \else
    \addtolength\topmargin{-2.0in}
  \fi
  \addtolength\topmargin{-.5\topmargin}
\fi
\@settopoint\topmargin
\if@twocolumn
  \setlength\marginparsep{10\p@}
\else
  \setlength\marginparsep{10\p@}
\fi
\setlength\marginparpush{5\p@}
\if@compatibility
    \setlength\oddsidemargin   {.5in}
    \setlength\evensidemargin  {1.5in}
    \setlength\marginparwidth {.75in}
  \if@twocolumn
     \setlength\oddsidemargin  {30\p@}
     \setlength\evensidemargin {30\p@}
     \setlength\marginparwidth {48\p@}
  \fi
  \if@stysize
    \if@twocolumn\else
      \setlength\oddsidemargin{0\p@}
      \setlength\evensidemargin{0\p@}
    \fi
  \fi
\else
  \setlength\@tempdima{\paperwidth}
  \addtolength\@tempdima{-\textwidth}
  \if@twoside
    \setlength\oddsidemargin{.4\@tempdima}
  \else
    \setlength\oddsidemargin{.5\@tempdima}
  \fi
  \addtolength\oddsidemargin{-1in}
  \setlength\evensidemargin{\paperwidth}
  \addtolength\evensidemargin{-2in}
  \addtolength\evensidemargin{-\textwidth}
  \addtolength\evensidemargin{-\oddsidemargin}
  \@settopoint\oddsidemargin % 1999.1.6
  \@settopoint\evensidemargin
  \if@twoside
    \setlength\marginparwidth{.6\@tempdima}
    \addtolength\marginparwidth{-.4in}
  \else
    \setlength\marginparwidth{.5\@tempdima}
    \addtolength\marginparwidth{-.4in}
  \fi
  \ifdim \marginparwidth >2in
    \setlength\marginparwidth{2in}
  \fi
  \@settopoint\marginparwidth
\fi
\setlength\footnotesep{0pt}%{.5\Cvs}%{6.65\p@}
\setlength{\skip\footins}{9\p@ \@plus 4\p@ \@minus 2\p@}


\setlength\floatsep{5.5mm \@plus 1.5mm \@minus 1.5mm}%
\setlength\textfloatsep{5.5mm \@plus 1.5mm \@minus 1.5mm}%

\setlength\intextsep{4mm \@plus 14.5mm \@minus 2.5mm
}%

%\setlength\floatsep    {12\p@ \@plus 2\p@ \@minus 2\p@}
%\setlength\textfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}
%\setlength\intextsep   {12\p@ \@plus 2\p@ \@minus 2\p@}


\setlength\dblfloatsep    {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dbltextfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\@fptop{0\p@ \@plus 1fil}
\setlength\@fpsep{8\p@ \@plus 2fil}
\setlength\@fpbot{0\p@ \@plus 1fil}
\setlength\@dblfptop{0\p@ \@plus 1fil}
\setlength\@dblfpsep{8\p@ \@plus 2fil}
\setlength\@dblfpbot{0\p@ \@plus 1fil}
\setlength\partopsep{2\p@ \@plus 1\p@ \@minus 1\p@}
\def\@listi{\leftmargin\leftmargini
  \parsep 4\p@ \@plus2\p@ \@minus\p@
  \topsep 8\p@ \@plus2\p@ \@minus4\p@
  \itemsep4\p@ \@plus2\p@ \@minus\p@}
\let\@listI\@listi
\@listi
\def\@listii{\leftmargin\leftmarginii
   \labelwidth\leftmarginii \advance\labelwidth-\labelsep
   \topsep  4\p@ \@plus2\p@ \@minus\p@
   \parsep  2\p@ \@plus\p@  \@minus\p@
   \itemsep\parsep}
\def\@listiii{\leftmargin\leftmarginiii
   \labelwidth\leftmarginiii \advance\labelwidth-\labelsep
   \topsep 2\p@  \@plus\p@\@minus\p@
   \parsep\z@
   \partopsep \p@ \@plus\z@ \@minus\p@
   \itemsep\topsep}
\def\@listiv {\leftmargin\leftmarginiv
              \labelwidth\leftmarginiv
              \advance\labelwidth-\labelsep}
\def\@listv  {\leftmargin\leftmarginv
              \labelwidth\leftmarginv
              \advance\labelwidth-\labelsep}
\def\@listvi {\leftmargin\leftmarginvi
              \labelwidth\leftmarginvi
              \advance\labelwidth-\labelsep}
%%%\endinput
%%
%% End of file `jbk10.clo'.
%%%%% end input jbk10.clo
\if@stysize
  \setlength\columnsep{2\Cwd}
\else
  \setlength\columnsep{10\p@}
\fi
\setlength\columnseprule{0\p@}
\setlength\lineskip{1\p@}
\setlength\normallineskip{1\p@}
\renewcommand{\baselinestretch}{}
\setlength\parskip{0\p@ \@plus \p@}
\setlength\parindent{1\Cwd}
\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301
\setcounter{topnumber}{2}
\setcounter{bottomnumber}{1}
\setcounter{totalnumber}{3}
\setcounter{dbltopnumber}{2}
\renewcommand{\topfraction}{.7}
\renewcommand{\bottomfraction}{.3}
\renewcommand{\textfraction}{.2}
\renewcommand{\floatpagefraction}{.5}
\renewcommand{\dbltopfraction}{.7}
\renewcommand{\dblfloatpagefraction}{.5}
\def\ps@plain{\let\@mkboth\@gobbletwo
   \let\ps@jpl@in\ps@plain
   \let\@oddhead\@empty
   \def\@oddfoot{\reset@font\hfil\thepage\hfil}%
   \let\@evenhead\@empty
   \let\@evenfoot\@oddfoot}
\let\ps@jpl@in\ps@plain
\def\ps@headnombre{\let\@mkboth\@gobbletwo
    \let\ps@jpl@in\ps@headnombre
  \def\@evenhead{\thepage\hfil}%
  \def\@oddhead{\hfil\thepage}%
  \let\@oddfoot\@empty\let\@evenfoot\@empty}
\def\ps@footnombre{\let\@mkboth\@gobbletwo
    \let\ps@jpl@in\ps@footnombre
  \def\@evenfoot{\thepage\hfil}%
  \def\@oddfoot{\hfil\thepage}%
  \let\@oddhead\@empty\let\@evenhead\@empty}


%%%
\newsavebox{\RAYOUT}
\savebox{\RAYOUT}{\normalsize%
\begin{minipage}{35\Cwd}\normalsize
\color{REYoutI}%
\noindent%%5
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
■□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□



\noindent%%10
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
■□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□



\noindent%%15
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
■□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□



\noindent%%20
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
■□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□



\noindent%%25
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
■□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□


\noindent%%28
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
□□□□□□□□□■□□□□□□□□□■□□□□□□□□□■□□□□□
\end{minipage}}






\if@Proof
 \def\@Rtop{\rlap{\smash{\rule[-\headsep]{0.05mm}{10mm}%
  \rule[-\headsep]{10mm}{0.05mm}}}}
 \def\@Ltop{\llap{\smash{\rule[-\headsep]{10mm}{0.05mm}%
  \rule[-\headsep]{0.05mm}{10mm}}}}
 \def\@Rbot{\rlap{\smash{\raisebox{1\footskip}
  {\rule[-10mm]{0.05mm}{10mm}\rule{10mm}{0.05mm}}}}}
 \def\@Lbot{\llap{\smash{\raisebox{1\footskip}
  {\rule{10mm}{0.05mm}\rule[-10mm]{0.05mm}{10mm}}}}}
%%%%
 \def\@Ctate{\relax}
\def\@Cyoko{\relax}
%%%
 \def\pot@jobname{\smash{\raise7mm\rlap{\LARGE\texttt{\jobname}}}}
\else
 \let\@Rtop\relax\let\@Ltop\relax\let\@Rbot\relax\let\@Lbot\relax\let\@Ctate\relax\let\@Cyoko\relax
 \let\pot@jobname\relax
\fi




\if@MASUME
 \def\@Rtop{\rlap{\smash{\rule[-\headsep]{0.05mm}{10mm}%
  \rule[-\headsep]{10mm}{0.05mm}}}}
 \def\@Ltop{\llap{\smash{\rule[-\headsep]{10mm}{0.05mm}%
  \rule[-\headsep]{0.05mm}{10mm}}}}
 \def\@Rbot{\rlap{\smash{\raisebox{1\footskip}
  {\rule[-10mm]{0.05mm}{10mm}\rule{10mm}{0.05mm}}}}}
% \def\@Lbot{\llap{\smash{\raisebox{1\footskip}
%  {\rule{10mm}{0.05mm}\rule[-10mm]{0.05mm}{10mm}}}}}
 \def\@Lbot{\smash{\raisebox{93.5mm}{\pushtowall{\hspace*{-.03125mm}\usebox{\RAYOUT}}}}\llap{\smash{\raisebox{1\footskip}
  {\rule{10mm}{0.05mm}\rule[-10mm]{0.05mm}{10mm}}}}}
%%%%
 \def\@Ctate{\relax}
\def\@Cyoko{\relax}
%%%
 \def\pot@jobname{\smash{\raise7mm\rlap{\LARGE\texttt{\jobname}}}}
\else
 \let\@Rtop\relax\let\@Ltop\relax\let\@Rbot\relax\let\@Lbot\relax\let\@Ctate\relax\let\@Cyoko\relax
 \let\pot@jobname\relax
\fi














\newdimen\HASIRAdimen
\HASIRAdimen=33mm %%( 12Q X 11倍)



\newcount\@BUNRUI
\ifnum\@BUNRUI=\z@
\pagenumbering{roman}%
\else
\pagenumbering{arabic}
\fi

\newif\ifROMANnumber 
\def\@ROMANnumber{%\ROMANnumbertrue
\ifROMANnumber
\pagenumbering{roman}%
\else
\pagenumbering{arabic}
\fi}


\if@twoside
   \def\ps@headings{%\let\ps@jpl@in\ps@headnombre
    \def\@evenhead{\@Ltop\small\hspace{12\JQ}{\slshape\thepage}\hskip24\JQ%
\underline{\hskip1zw%
\setbox0=\hbox{\leftmark}%
\ifdim\wd0 >\HASIRAdimen
\leftmark\else%
\hbox to\HASIRAdimen{\hss\ELEVENjidori{\leftmark}\hss}%
\fi%
\hskip1zw}%
%
\hfill\@Rtop}%
    \def\@oddhead{\@Ltop\hfill\small
\underline{\hskip1zw%
\ifnum\c@section>0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\setbox0=\hbox{\rightmark}%
\ifdim\wd0 >\HASIRAdimen
\rightmark\else%
\hbox to\HASIRAdimen{\hss\ELEVENjidori{\rightmark}\hss}%
\fi%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\else
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\setbox0=\hbox{\leftmark}%
\ifdim\wd0 >\HASIRAdimen
\leftmark\else%
\hbox to\HASIRAdimen{\hss\ELEVENjidori{\leftmark}\hss}%
\fi%
\fi%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\hskip1zw}%
\hskip24\JQ{\slshape\thepage}\hskip12\JQ\@Rtop}%
    \def\@evenfoot{\@Lbot\small\hfill\@Rbot}%
    \def\@oddfoot{\@Lbot\small\hfill\@Rbot}%
    \let\@mkboth\markboth
  \def\chaptermark##1{\markboth{%
     \ifnum \c@secnumdepth >\m@ne
         \if@mainmatter
         \thechapter.\hskip1zw\nobreak%
         \fi
     \fi
     {##1}}{}}%
  \def\sectionmark##1{\markright{%
     \ifnum \c@secnumdepth >\z@ \thesection\hskip1zw\nobreak
\fi
     ##1}}%
  }
%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   \def\ps@Rheadings{\renewcommand{\thepage}{\@roman\c@page}%\pagenumbering{roman}%\let\ps@jpl@in\ps@headnombre
    \def\@evenhead{\@Ltop\small\hspace{12\JQ}{\slshape\thepage}\hskip24\JQ%
\underline{\hskip1zw%
\setbox0=\hbox{\leftmark}%
\ifdim\wd0 >\HASIRAdimen
\leftmark\else%
\hbox to\HASIRAdimen{\hss\ELEVENjidori{\leftmark}\hss}%
\fi%
\hskip1zw}%
%
\hfill\@Rtop}%
    \def\@oddhead{\@Ltop\hfill\small
\underline{\hskip1zw%
\setbox0=\hbox{\rightmark}%
\ifdim\wd0 >\HASIRAdimen
\rightmark\else%
\hbox to\HASIRAdimen{\hss\ELEVENjidori{\rightmark}\hss}%
\fi%
\hskip1zw}%
\hskip24\JQ{\slshape\thepage}\hskip12\JQ\@Rtop}%
    \def\@evenfoot{\@Lbot\small\hfill\@Rbot}%
    \def\@oddfoot{\@Lbot\small\hfill\@Rbot}%
    \let\@mkboth\markboth
  \def\chaptermark##1{\markboth{%
     \ifnum \c@secnumdepth >\m@ne
         \if@mainmatter
         \thechapter.\hskip1zw\nobreak%
         \fi
     \fi
     {##1}}{}}%
  \def\sectionmark##1{\markright{%
     \ifnum \c@secnumdepth >\z@ \thesection\hskip1zw\nobreak
\fi
     ##1}}%
  }
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  \def\ps@CHAPheadings{\let\ps@jpl@in\ps@headnombre
    \def\@evenhead{\@Ltop\small\hspace{12\JQ}\hskip24\JQ\mbox{}\hfill\@Rtop}%
    \def\@oddhead{\@Ltop\hfill\small\mbox{}\hskip12\JQ\hskip12\JQ\@Rtop}%
    \def\@evenfoot{\@Lbot\small\hfill\@Rbot}%
    \def\@oddfoot{\@Lbot\small\hfill\@Rbot}%
  }
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   \def\ps@APPheadings{\let\ps@jpl@in\ps@headnombre
    \def\@evenhead{\@Ltop\small\hspace{12\JQ}{\slshape\thepage}\hskip24\JQ%
\underline{\hskip1zw%
\setbox0=\hbox{\leftmark}%
\ifdim\wd0 >\HASIRAdimen
\leftmark\else%
\hbox to\HASIRAdimen{\hss\ELEVENjidori{\leftmark}\hss}%
\fi%
\hskip1zw}%
%
\hfill\@Rtop}%
    \def\@oddhead{\@Ltop\hfill\small
\underline{\hskip1zw%
\setbox0=\hbox{\rightmark}%
\ifdim\wd0 >\HASIRAdimen
\rightmark\else%
\hbox to\HASIRAdimen{\hss\ELEVENjidori{\rightmark}\hss}%
\fi%
\hskip1zw}%
\hskip24\JQ{\slshape\thepage}\hskip12\JQ\@Rtop}%
    \def\@evenfoot{\@Lbot\small\hfill\@Rbot}%
    \def\@oddfoot{\@Lbot\small\hfill\@Rbot}%
    \let\@mkboth\markboth
  \def\chaptermark##1{\markboth{%
%     \ifnum \c@secnumdepth >\m@ne
%         \if@mainmatter
%         \thechapter.\hskip1zw\nobreak%
%         \fi
%     \fi
     {##1}}{}}%
  \def\sectionmark##1{\markright{%
     \ifnum \c@secnumdepth >\z@ \thesection\hskip1zw\nobreak
\fi
     ##1}}%
  }
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\else % if not twoside
  \def\ps@headings{\let\ps@jpl@in\ps@headnombre
    \let\@oddfoot\@empty
    \def\@oddhead{{\rightmark}\hfil\thepage}%
    \let\@mkboth\markboth
\def\chaptermark##1{\markright{%
   \ifnum \c@secnumdepth >\m@ne
         \if@mainmatter
       \@chapapp\thechapter\@chappos\hskip1zw
         \fi
   \fi
   ##1}}%
  }
\fi
\if@twoside
  \def\ps@bothstyle{\let\ps@jpl@in\ps@footnombre
    \def\@evenhead{\leftmark\hfil}% right page
    \def\@evenfoot{\thepage\hfil}% right page
    \def\@oddhead{\hfil\rightmark}% left page
    \def\@oddfoot{\hfil\thepage}% left page
  \let\@mkboth\markboth
\def\chaptermark##1{\markboth{%
     \ifnum \c@secnumdepth >\m@ne
         \if@mainmatter
         \@chapapp\thechapter\@chappos\hskip1zw
         \fi
     \fi
     ##1}{}}%
  \def\sectionmark##1{\markright{%
     \ifnum \c@secnumdepth >\z@ \thesection.\hskip1zw\fi
     ##1}}%
  }
\else % if one column
  \def\ps@bothstyle{\let\ps@jpl@in\ps@footnombre
    \def\@oddhead{\hfil\rightmark}%
    \def\@oddfoot{\hfil\thepage}%
    \let\@mkboth\markboth
  \def\chaptermark##1{\markright{%
     \ifnum \c@secnumdepth >\m@ne
         \if@mainmatter
         \@chapapp\thechapter\@chappos\hskip1zw
         \fi
     \fi
     ##1}}%
  }
\fi
\def\ps@myheadings{\let\ps@jpl@in\ps@plain%
  \let\@oddfoot\@empty\let\@evenfoot\@empty
  \def\@evenhead{\thepage\hfil\leftmark}%
  \def\@oddhead{{\rightmark}\hfil\thepage}%
  \let\@mkboth\@gobbletwo
  \let\chaptermark\@gobble
  \let\sectionmark\@gobble
}
\if@compatibility
\newenvironment{titlepage}
    {%
      \cleardoublepage
     \if@twocolumn\@restonecoltrue\onecolumn
     \else\@restonecolfalse\newpage\fi
     \thispagestyle{empty}%
     \setcounter{page}\z@
    }%
    {\if@restonecol\twocolumn\else\newpage\fi
    }
\else
\newenvironment{titlepage}
    {%
      \cleardoublepage
      \if@twocolumn
        \@restonecoltrue\onecolumn
      \else
        \@restonecolfalse\newpage
      \fi
      \thispagestyle{empty}%
      \setcounter{page}\@ne
    }%
    {\if@restonecol\twocolumn \else \newpage \fi
     \if@twoside\else
        \setcounter{page}\@ne
     \fi
    }
\fi
\def\p@thanks#1{\footnotemark
  \protected@xdef\@thanks{\@thanks
    \protect{\noindent$\m@th^\thefootnote$~#1\protect\par}}}
\if@titlepage
  \newcommand{\maketitle}{\begin{titlepage}%
  \let\footnotesize\small
  \let\footnoterule\relax
  \let\footnote\thanks
  \null\vfil
  \vskip 60\p@
  \begin{center}%
    {\LARGE \@title \par}%
    \vskip 3em%
    {\Large
     \lineskip .75em%
      \begin{tabular}[t]{c}%
        \@author
      \end{tabular}\par}%
      \vskip 1.5em%
    {\large \@date \par}%       % Set date in \large size.
  \end{center}\par
  \@thanks\vfil\null
  \end{titlepage}%
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\p@thanks\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
  }%
\else
  \newcommand{\maketitle}{\par
  \begingroup
    \renewcommand{\thefootnote}{\fnsymbol{footnote}}%
    \def\@makefnmark{\hbox{\ifydir $\m@th^{\@thefnmark}$
      \else\hbox{\yoko$\m@th^{\@thefnmark}$}\fi}}%
     \long\def\@makefntext##1{\parindent 1em\noindent
       \hbox to1.8em{\hss$\m@th^{\@thefnmark}$}##1}%
    \if@twocolumn
      \ifnum \col@number=\@ne \@maketitle
      \else \twocolumn[\@maketitle]%
      \fi
    \else
      \newpage
      \global\@topnum\z@   % Prevents figures from going at top of page.
      \@maketitle
    \fi
     \thispagestyle{jpl@in}\@thanks
  \endgroup
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\p@thanks\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
  }
  \def\@maketitle{%
  \newpage\null
  \vskip 2em%
  \begin{center}%
  \let\footnote\thanks
    {\LARGE \@title \par}%
    \vskip 1.5em%
    {\large
      \lineskip .5em%
      \begin{tabular}[t]{c}%
        \@author
      \end{tabular}\par}%
    \vskip 1em%
    {\large \@date}%
  \end{center}%
  \par\vskip 1.5em}
\fi
\newcommand*{\chaptermark}[1]{}
\setcounter{secnumdepth}{4}
\newcounter{part}
\newcounter{chapter}
\newcounter{section}[chapter]
\newcounter{subsection}[section]
\newcounter{subsubsection}[subsection]
\newcounter{paragraph}[subsubsection]
\newcounter{subparagraph}[paragraph]
\renewcommand{\thepart}{\@Roman\c@part}
\renewcommand{\thechapter}{\@arabic\c@chapter}
\renewcommand{\thesection}{\thechapter.\@arabic\c@section}
\renewcommand{\thesubsection}{\thesection.\@arabic\c@subsection}
\renewcommand{\thesubsubsection}{\hbox
  to2zw{{\rm(}\hfill\@arabic\c@subsubsection\hfill{\rm)}}}
%\renewcommand{\thesubsubsection}{{\@arabic\c@subsubsection}}
\renewcommand{\theparagraph}{\hbox to2zw{{\rm(}\hfill\@alph\c@paragraph\hfill{\rm)}}}
\renewcommand{\thesubparagraph}{%
   \theparagraph.\@arabic\c@subparagraph}
\newcommand{\@chapapp}{\prechaptername}
\newcommand{\@chappos}{\postchaptername}
\newcommand\frontmatter{%
  \if@openright \cleardoublepage \else \clearpage \fi
  \@mainmatterfalse\pagenumbering{roman}}
\newcommand{\mainmatter}{%
  \if@openright \cleardoublepage \else \clearpage \fi
  \@mainmattertrue\pagenumbering{arabic}}
\newcommand{\backmatter}{%
  \if@openright \cleardoublepage \else \clearpage \fi
  \@mainmatterfalse}
\newcommand{\part}{%
  \if@openright \cleardoublepage \else \clearpage \fi
  \thispagestyle{empty}%
  \if@twocolumn\onecolumn\@tempswatrue\else\@tempswafalse\fi
  \null\vfil
  \secdef\@part\@spart}
\def\@part[#1]#2{%
  \ifnum \c@secnumdepth >-2\relax
    \refstepcounter{part}%
    \addcontentsline{toc}{part}{%
       \prepartname\thepart\postpartname\hspace{1em}#1}%
  \else
    \addcontentsline{toc}{part}{#1}%
  \fi
  \markboth{}{}%
  {\centering
   \interlinepenalty\@M\reset@font
   \ifnum \c@secnumdepth >-2\relax
     \huge\bfseries\prepartname\thepart\postpartname
     \par\vskip20\p@
   \fi
   \Huge\bfseries#2\par}%
   \@endpart}
\def\@spart#1{{%
  \centering
  \interlinepenalty\@M\reset@font
  \Huge\bfseries#1\par}%
  \@endpart}
\def\@endpart{\vfil\newpage
   \if@twoside\null\thispagestyle{empty}\newpage\fi
   \if@tempswa\twocolumn\fi}

\newcommand{\chapter}{%%%
  \if@openright\clearpage\else\clearpage\fi
%
  \thispagestyle{CHAPheadings}%
  \global\@topnum\z@
  \@afterindentfalse
  \secdef\@chapter\@schapter}

%\def\addcontentsline#1#2#3{%
%  \addtocontents{#1}{\protect\contentsline{#2}{#3}{\thepage}}★\nopagebreak[4]}

\def\@chapter[#1]#2{%
  \ifnum \c@secnumdepth >\m@ne
    \if@mainmatter
    \refstepcounter{chapter}%
    \typeout{\@chapapp\space\thechapter\space\@chappos}%
    \addcontentsline{toc}{chapter}%
      {\protect\numberline{\thechapter.}\protect\mokuSEVENjidori{#1}}%
    \else\addcontentsline{toc}{chapter}{\protect\mokuSEVENjidori{#1}}\fi
  \else
    \addcontentsline{toc}{chapter}{\protect\mokuSEVENjidori{#1}}%
  \fi
  \chaptermark{#1}%
  \addtocontents{lof}{\protect\addvspace{10\p@}}%
  \addtocontents{lot}{\protect\addvspace{10\p@}}%
  \@makechapterhead{#2}%\@afterheading%
\renewcommand{\thepage}{\@arabic\c@page}%
\ifnum\c@chapter=1 \setcounter{page}{1}\else\fi%
}






%%% 章見出し 7行どり
\newdimen\CHAPheight
\CHAPheight=6\baselineskip 
\addtolength{\CHAPheight}{\topskip}%

\newbox\CHAPht


\newdimen\CHAPwidth

%%%%%% 旧コロナスタイルのサイズ指定から，移植した
%%%%%% \fontsize{14}{15}
%%%%%%
\def\@makechapterhead#1{\normalsize\baselineskip25\h%%
 \vbox to \CHAPheight
  {\parindent\z@\vskip5mm
%   \raggedright
   \reset@font%\huge\bfseries
   \leavevmode
   \ifnum \c@secnumdepth >\m@ne
     \setlength\@tempdima{\linewidth}%
    \if@mainmatter
     \setbox\z@\hbox{\textsl{\bfseries\fontsize{\@xxvpt}{28}\selectfont\thechapter}}%
     \addtolength\@tempdima{-\wd\z@}%
   \hfil{\smash{\raisebox{-2mm}{\unhbox\z@}}\nobreak
    \fi
%%%%%%%%%%%%%%%%%%%%%%%%%
\setbox\CHAPwidth=\hbox{\bfseries\fontsize{14}{15}\selectfont\shortstack{#1}}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
\ifdim\ht\CHAPwidth>\baselineskip%294pt
%%% 改行するとき
{\bfseries\fontsize{14}{15}\selectfont\smash{\rule[-9.5mm]{.4mm}{14mm}\hskip.9pt\rule[-9.5mm]{.12mm}{14mm}}\hspace{1zw}\hsize\@tempdima\raisebox{-40pt}{\shortstack[l]{#1}}
}%
%%%
\else
%%% 改行なし
{\bfseries\fontsize{14}{15}\selectfont\smash{\rule[-9.5mm]{.4mm}{14mm}\hskip.9pt\rule[-9.5mm]{.12mm}{14mm}}\hspace{1zw}\hsize\@tempdima\raisebox{-27.5pt}{\SEVENjidori{#1}}}%
\fi
%%%
   \else
     \SEVENjidori{#1}\relax
   \fi
\vfill}}%
}






%%%% 20Q  中ゴ 7字ﾄﾞﾘ 5行分 天地左右中央
%%% 付録、文献の章立てパターンは同じ
\newdimen\SCHAPheight
\SCHAPheight=4\baselineskip 
\addtolength{\SCHAPheight}{\topskip}%


\def\@makeschapterhead#1{\clearpage%
\normalsize\baselineskip25\h%\hbox{}%
\vbox to \SCHAPheight
  {\vfill\parindent\z@
   \raggedright
   \reset@font\huge\bfseries
   \leavevmode
   \setlength\@tempdima{\linewidth}%
   \centerline{%\hsize\@tempdima
\fontsize{20\JQ}{32H}\selectfont\SEVENjidori{#1}}\par\vfill
%\smash{.\hskip30mm.\hskip40mm.}
}%\vskip3\Cvs
}





\def\@makeschapterhead#1{\clearpage%
\normalsize\baselineskip25\h%\hbox{}%
\vbox to \SCHAPheight
  {%\vfill
\vskip2\Cvs\parindent\z@
   \raggedright
   \reset@font\huge\bfseries
   \leavevmode
   \setlength\@tempdima{\linewidth}%
   \centerline{%\hsize\@tempdima
\fontsize{20\JQ}{32H}\selectfont\SEVENjidori{#1}}\par\vfill
%\smash{.\hskip30mm.\hskip40mm.}
}%\vskip3\Cvs
}



\def\@schapter#1{%
  \@makeschapterhead{#1}%\@afterheading
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%% 欧文文字列の章見出し \Echapter \Echapter* の設定 %%%%%
%%%% 字ドリなし のセンタリング

\newcommand{\Echapter}{%%%
  \if@openright\clearpage\else\clearpage\fi
%
  \thispagestyle{CHAPheadings}%
  \global\@topnum\z@
  \@afterindentfalse
  \secdef\@Echapter\@Eschapter}


\def\@Echapter[#1]#2{%
  \ifnum \c@secnumdepth >\m@ne
    \if@mainmatter
    \refstepcounter{chapter}%
    \typeout{\@chapapp\space\thechapter\space\@chappos}%
    \addcontentsline{toc}{chapter}%
      {\protect\numberline{\thechapter.}{\hbox to7zw{\hfill#1\hfill}}}%
    \else\addcontentsline{toc}{chapter}{\hbox to7zw{\hfill#1\hfill}}\fi
  \else
    \addcontentsline{toc}{chapter}{\hbox to7zw{\hfill#1\hfill}}%
  \fi
  \chaptermark{\hfill#1\hfill}%
  \addtocontents{lof}{\protect\addvspace{10\p@}}%
  \addtocontents{lot}{\protect\addvspace{10\p@}}%
  \@makeEchapterhead{#2}%\@afterheading%
\renewcommand{\thepage}{\@arabic\c@page}%
\ifnum\c@chapter=1 \setcounter{page}{1}\else\fi%
}


\def\@makeEchapterhead#1{\normalsize\baselineskip25\h%%
 \vbox to \CHAPheight
  {\parindent\z@\vskip5mm
%   \raggedright
   \reset@font%\huge\bfseries
   \leavevmode
   \ifnum \c@secnumdepth >\m@ne
     \setlength\@tempdima{\linewidth}%
    \if@mainmatter
     \setbox\z@\hbox{\textsl{\bfseries\fontsize{\@xxvpt}{28}\selectfont\thechapter}}%
     \addtolength\@tempdima{-\wd\z@}%
   \hfil{\smash{\raisebox{-2mm}{\unhbox\z@}}\nobreak
    \fi
%%%%%%%%%%%%%%%%%%%%%%%%%
\setbox\CHAPwidth=\hbox{\bfseries\fontsize{14}{15}\selectfont\shortstack{#1}}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
\ifdim\ht\CHAPwidth>\baselineskip%294pt
%%% 改行するとき
{\bfseries\fontsize{14}{15}\selectfont\smash{\rule[-9.5mm]{.4mm}{14mm}\hskip.9pt\rule[-9.5mm]{.12mm}{14mm}}\hspace{1zw}\hsize\@tempdima\raisebox{-40pt}{\shortstack[l]{#1}}
}%
%%%
\else
%%% 改行なし
{\bfseries\fontsize{14}{15}\selectfont\smash{\rule[-9.5mm]{.4mm}{14mm}\hskip.9pt\rule[-9.5mm]{.12mm}{14mm}}\hspace{1zw}\hsize\@tempdima\raisebox{-27.5pt}{{#1}}}%
\fi
%%%
   \else
     {#1}\relax
   \fi
\vfill}}%
}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\def\@makeEchapterhead#1{\normalsize\baselineskip25\h%%
 \vbox to \CHAPheight
  {\parindent\z@\vskip5mm
%   \raggedright
   \reset@font%\huge\bfseries
   \leavevmode
   \ifnum \c@secnumdepth >\m@ne
     \setlength\@tempdima{\linewidth}%
    \if@mainmatter
     \setbox\z@\hbox{\textsl{\bfseries\fontsize{\@xxvpt}{28}\selectfont\thechapter}}%
     \addtolength\@tempdima{-\wd\z@}%
   \hfil{\smash{\raisebox{-2mm}{\unhbox\z@}}\nobreak
    \fi
%%%%%%%%%%%%%%%%%%%%%%%%%
\setbox\CHAPwidth=\hbox{\bfseries\fontsize{14}{15}\selectfont\shortstack{#1}}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 条件1 ： 7zwより横幅は長く，2行以上のとき
\ifdim\wd\CHAPwidth>7.4zw
\ifdim\ht\CHAPwidth>\baselineskip%294pt
%%% 改行するとき
{\bfseries\fontsize{14}{15}\selectfont\smash{\rule[-9.5mm]{.4mm}{14mm}\hskip.9pt\rule[-9.5mm]{.12mm}{14mm}}\hspace{1zw}\hsize\@tempdima\raisebox{-40pt}{\shortstack[l]{#1}}
}%
%%%
\else
%% 条件2 ： 7zwより横幅は長く，1行のとき
%%% 改行なし
{\bfseries\fontsize{14}{15}\selectfont\smash{\rule[-9.5mm]{.4mm}{14mm}\hskip.9pt\rule[-9.5mm]{.12mm}{14mm}}\hspace{1zw}\hsize\@tempdima\raisebox{-27.5pt}{{#1}}}%
\fi
%%%
\else%%% +
%% 条件3 ： 7zwより横幅は短く，1行のとき
{\bfseries\fontsize{14}{15}\selectfont\smash{\rule[-9.5mm]{.4mm}{14mm}\hskip.9pt\rule[-9.5mm]{.12mm}{14mm}}\hspace{1zw}\hsize\@tempdima\raisebox{-27.5pt}{\hbox
to7zw{\hfill#1\hfill}}}%
\fi%%%%% +
   \else
     {#1}\relax
   \fi
\vfill}}%
}








%%%% 20Q  中ゴ 7字ﾄﾞﾘ 5行分 天地左右中央
%%% 付録、文献の章立てパターンは同じ
%\newdimen\SCHAPheight
%\SCHAPheight=4\baselineskip 
%\addtolength{\SCHAPheight}{\topskip}%


\def\@makeEschapterhead#1{\clearpage%
\normalsize\baselineskip25\h%\hbox{}%
\vbox to \SCHAPheight
  {%\vfill
\vskip2\Cvs\parindent\z@
   \raggedright
   \reset@font\huge\bfseries
   \leavevmode
   \setlength\@tempdima{\linewidth}%
%%%%%%%%%%%%%%%%%%%%%%%%%
\setbox\CHAPwidth=\hbox{\bfseries\fontsize{14}{15}\selectfont\shortstack{#1}}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
   \centerline{%\hsize\@tempdima
\ifdim\wd\CHAPwidth>7.4zw
\fontsize{20\JQ}{32H}\selectfont\raisebox{-2.5mm}{\smash{\shortstack{#1}}}
\else
\fontsize{20\JQ}{32H}\selectfont\raisebox{-2.5mm}{\smash{\hbox to7zw{\hfill#1\hfill}}}
\fi
}%\par
\vfill
%\smash{.\hskip30mm.\hskip40mm.}
}%\vskip3\Cvs
}


\def\@Eschapter#1{%
  \@makeEschapterhead{#1}%\@afterheading
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



\newdimen\ESECTwd

%%% %%%%%%%%% 
%%%  欧文用 節 \section に関する マクロ は \Esection
%%%  項はセンタリングでないので、作る必要ないと思う
%%% %%%%%%%%% 

%%% %%%%%%%%% 
\def\@startEsection#1#2#3#4#5#6{%
%
%
\if@noskipsec \leavevmode \fi
   \par \@tempskipa #4\relax
   \@afterindenttrue
   \ifdim \@tempskipa <\z@ \@tempskipa -\@tempskipa \@afterindentfalse\fi %% >
   \if@nobreak
    \everypar{}%
   \else
    \addpenalty\@secpenalty
     \ifnum #2=\@ne
       \vskip-\prevdepth \prevdepth\z@ \vskip\Cvs
       \advance\@tempskipa-\Cvs \vspace*{\@tempskipa}%
     \else
      \addvspace\@tempskipa
     \fi
   \fi
 \@ifstar{\@Essect{#3}{#4}{#5}{#6}}{\@dblarg{\@Esect{#1}{#2}{#3}{#4}{#5}{#6}}}}


\def\@Esect#1#2#3#4#5#6[#7]#8{%
  \ifnum #2>\c@secnumdepth
    \let\@Esvsec\@empty
  \else
    \refstepcounter{#1}%
%    \protected@edef\@svsec{\fontsize{16\Q}{18H}\selectfont\@seccntformat{#1}\relax}%
    \protected@edef\@Esvsec{\selectfont\@seccntformat{#1}\relax}%
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
%%%%
 \setbox\@tempboxb\hbox{\large#6{%
      \@hangfrom{%
\hskip #3\relax{\csname #2@font\endcsname \@Esvsec}}}}%\the\wd\@tempboxb
%%
\setbox\SECTwd=\hbox{%
\begingroup\noindent\large%
    #6{%
      \@hangfrom{%
\hskip #3\relax{\csname #2@font\endcsname \@Esvsec}}%★%
       \interlinepenalty \@M %\@secjidori
\shortstack[l]{%
\noindent
#8}\@@par}%
   \endgroup
}
\setbox\ESECTwd=\hbox{\large\bfseries
\shortstack[l]{%
\noindent
#8}%
}%%% \the\wd\ESECTwd #8 の文字列の長さを見たいとき
%%%%
  \ifdim \wd\ESECTwd > 79.66847pt% large\bfseries のサイズで、7字を計算した
%   \noindent%
%{\begingroup\noindent
%      #6{%
%        \@hangfrom{\hskip #3\relax\@Esvsec}%★2%
%          \interlinepenalty \@M 
%\noindent\hangindent\wd\@tempboxb\hangafter=1
%#8\@@par}%
%    \endgroup}
%%%%%%%%%
  \ifdim \ht\SECTht > \baselineskip
   \hfil\parbox[c]{\wd\SECTwd}%
{\begingroup\noindent
      #6{%
        \@hangfrom{\hskip #3\relax\@Esvsec}%★3%
          \interlinepenalty \@M 
\noindent\hangindent\wd\@tempboxb\hangafter=1
#8\@@par%\prevdepth\z@
}%
    \endgroup}
\vskip-\prevdepth \prevdepth\z@ %
%\vskip\Cvs
%       \advance\@tempskipa-\Cvs \vspace*{\@tempskipa}%
  \else
%%%%%%%%%
    \noindent\begingroup\noindent\hfil
      #6{%
        \@hangfrom{\hskip #3\relax\@Esvsec}%
          \interlinepenalty \@M 
#8\@@par}%
    \endgroup
%%%%%%%%%%%% +1
\fi
\else
%%%%%
    \noindent\begingroup\noindent\hfil
      #6{%
        \@hangfrom{\hskip #3\relax\@Esvsec}%
          \interlinepenalty \@M 
%% 処理C
\hbox to7zw{\hfill#8\hfill}\@@par}%
    \endgroup
%%%%%
\fi%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \csname #1mark\endcsname{\hfill#7\hfill}%
%%%%%%%%55
\setbox\ESECTwd=\hbox{#7}%
\ifdim \wd\ESECTwd >  7zw
    \addcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      {#7}}%
\else%
    \addcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      \protect\hbox to7zw{\hfill#7\hfill}}%
\fi%
%%%%%%55
  \else
    \def\@Esvsechd{%
      #6{\hskip #3\relax
      \@Esvsec #8}%
      \csname #1mark\endcsname{\hfill#7\hfill}%
      \addcontentsline{toc}{#1}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        \protect\hbox to7zw{\hfill #7\hfill}}}%
  \fi
  \@Exsect{#5}}
\def\@Exsect#1{%
  \@tempskipa #1\relax
  \ifdim \@tempskipa>\z@
    \par \nobreak
    \vskip \@tempskipa
    \@afterheading
  \else
    \@nobreakfalse
    \global\@noskipsectrue
    \everypar{%
      \if@noskipsec
        \global\@noskipsecfalse
       {\setbox\z@\lastbox}%
        \clubpenalty\@M
        \begingroup \@Esvsechd \endgroup
        \unskip
        \@tempskipa #1\relax
        \hskip -\@tempskipa
      \else
        \clubpenalty \@clubpenalty
        \everypar{}%
      \fi}%
  \fi
  \ignorespaces}
\def\@Eseccntformat#1{\csname the#1\endcsname\quad}

\def\@Essect#1#2#3#4#5{%
  \@tempskipa #3\relax
  \ifdim \@tempskipa>\z@
%%%
\setbox\SECTwd=\hbox{%
\begingroup\noindent
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M %
\shortstack[l]{
\noindent
#5}\@@par}%
    \endgroup
}
%%%%
\setbox\ESECTwd=\hbox{\large\bfseries
\shortstack[l]{%
\noindent
#5}%
}%%% \the\wd\ESECTwd #5 の文字列の長さを見たいとき
%%%%
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  \ifdim \wd\SECTwd > 79.66847pt% large\bfseries のサイズで、7字を計算した%\columnwidth
  \ifdim \wd\SECTwd > \columnwidth
   \noindent%
{\begingroup
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M 
\noindent%\hangindent\wd\@tempboxb\hangafter=1
#5\@@par}%
    \endgroup}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\else
    \noindent\begingroup\hfil
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M {#5}\@@par}%
    \endgroup
\fi
  \else
    \def\@Esvsechd{#4{\hskip #1\relax #5}}%
  \fi
  \@Exsect{#3}}




%%%%% 見出し和文文字はゴシック、欧文はボールド
%%% 節=\section は センタリング
 \newcommand{\Esection}{\@startEsection{section}{1}{0zw}%
   {1\Cvs \@plus.1mm \@minus.1mm}%
   {1\Cvs \@plus.1mm \@minus.1mm}%
   {\reset@font\large%\slshape
%\bfseries%\FutogoXvi%\HelveXvi
%\gt\sffamily
\bfseries
\mathversion{bold}%
%\fontsize{28Q}{32H}\selectfont
}}


%%%%% 欧文用 節 %%% END


%%%% 欧文用 項 

\newdimen\ESUBSECTwd

\def\@startEsectionB#1#2#3#4#5#6{\if@noskipsec \leavevmode \fi
  \par  \@tempskipa #4\relax
  \@afterindenttrue
  \ifdim \@tempskipa <\z@    \@tempskipa -\@tempskipa \@afterindentfalse  \fi
  \if@nobreak
    \everypar{}%
  \else
    \addpenalty\@secpenalty
\ifnum #2=\@ne
       \vskip-\prevdepth \prevdepth\z@ \vskip\Cvs
       \advance\@tempskipa-\Cvs \vspace*{\@tempskipa}%
     \else
\addvspace\@tempskipa
\fi
  \fi
  \@ifstar
    {\@EssectB{#3}{#4}{#5}{#6}}%
    {\@dblarg{\@EsectB{#1}{#2}{#3}{#4}{#5}{#6}}}}

\def\@EsectB#1#2#3#4#5#6[#7]#8{%
  \ifnum #2>\c@secnumdepth
    \let\@EsvsecB\@empty
  \else
    \refstepcounter{#1}%
    \protected@edef\@EsvsecB{%\protect\rule{0mm}{21.75mm}
\@EseccntformatB{#1}\relax}%
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% koko
\setbox\ESUBSECTwd=\hbox{\normalsize\bfseries
\shortstack[l]{%
\noindent
#8}%
}%%% \the\wd\ESUBSECTwd #8 の文字列の長さを見たいとき
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\ifdim \wd\ESUBSECTwd >7zw
%%
   \begingroup
      #6{%
        \@hangfrom{\hskip #3\relax\@EsvsecB}%
          \interlinepenalty \@M
%\protect\SEVENjidori
{#8}\@@par}%
    \endgroup%
%%
\else
%%
   \begingroup
      #6{%
        \@hangfrom{\hskip #3\relax\@EsvsecB}%
          \interlinepenalty \@M
\hbox to7zw{\hfill#8\hfill}\@@par}%
    \endgroup%
\fi
%%%%%
    \csname #1mark\endcsname{#7}%
%%%%%%%%%
\setbox\ESUBSECTwd=\hbox{#7}%
\ifdim \wd\ESUBSECTwd >  7zw
%%%%%%%%
    \addcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      {#7}}%
\else%
    \addcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      \hbox to7zw{\hfill#7\hfill}}%
\fi%
%%%%%%%%
  \else
    \def\@EsvsechdB{%
      #6{\hskip #3\relax
      \@EsvsecB #8}%
      \csname #1mark\endcsname{#7}%
      \addcontentsline{toc}{#1}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        #7}}%
  \fi
  \@ExsectB{#5}}
\def\@ExsectB#1{%
  \@tempskipa #1\relax
  \ifdim \@tempskipa>\z@
    \par \nobreak
    \vskip \@tempskipa
    \@afterheading
  \else
    \@nobreakfalse
    \global\@noskipsectrue
    \everypar{%
      \if@noskipsec
        \global\@noskipsecfalse
       {\setbox\z@\lastbox}%
        \clubpenalty0%\@M
        \begingroup \@svsechd \endgroup
        \unskip
        \@tempskipa #1\relax
        \hskip -\@tempskipa
      \else
        \clubpenalty \@clubpenalty
        \everypar{}%
      \fi}%
  \fi
  \ignorespaces}
%\def\@seccntformatA#1{\protect\SECTUP{\csname the#1\endcsname\quad}}
\def\@EseccntformatB#1{\csname the#1\endcsname\hskip1zw
}
\def\@EssectB#1#2#3#4#5{%
  \@tempskipa #3\relax
  \ifdim \@tempskipa>\z@
%%%%%%%%%%%%%%%%%%%55
\setbox\ESUBSECTwd=\hbox{\normalsize\bfseries
\shortstack[l]{%
\noindent
#5}%
}%%% \the\wd\ESUBSECTwd #8 の文字列の長さを見たいとき
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\ifdim \wd\ESUBSECTwd >7zw
%%%%%%%%%%%%%%%%
    \begingroup
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M #5\@@par}%
    \endgroup
\else
    \begingroup
      #4{%
        \@hangfrom{\hskip #1}%
%          \interlinepenalty \@M \hbox to7zw{\hfill#5\hfill}\@@par}%
          \interlinepenalty \@M #5\@@par}%
    \endgroup
\fi
%%%%%%%%%%%%%%%%%%%%
  \else
    \def\@EsvsechdB{#4{\hskip #1\relax #5}}%
  \fi
  \@ExsectB{#3}}
\newif\if@afterindent \@afterindenttrue
\def\@afterheading{%
  \@nobreaktrue
  \everypar{%
    \if@nobreak
      \@nobreakfalse
      \clubpenalty0 %\@M
      \if@afterindent \else
        {\setbox\z@\lastbox}%
      \fi
    \else
      \clubpenalty \@clubpenalty
      \everypar{}%
    \fi}}








\newcommand{\Esubsection}{\@startEsectionB{subsection}{2}{1zw}%
%   {1.5\Cvs \@plus.5\Cdp \@minus.2\Cdp}%
%   {.5\Cvs \@plus.3\Cdp}%
   {1\Cvs \@plus.1mm \@minus.1mm}%
   {.0001mm \@plus.1mm \@minus.1mm}%
   {\reset@font\bfseries}}



%%%% 欧文用 項 %%% END




%\newdimen\MIDASIdimen
%\newbox\@tempboxa
\newbox\@tempboxb

\newdimen\SECTht
\newdimen\SECTwd


%%% 和文用 startsection
\def\@startsection#1#2#3#4#5#6{\if@noskipsec \leavevmode \fi
   \par \@tempskipa #4\relax
   \@afterindenttrue
   \ifdim \@tempskipa <\z@ \@tempskipa -\@tempskipa \@afterindentfalse\fi %% >
   \if@nobreak
    \everypar{}%
   \else
    \addpenalty\@secpenalty
     \ifnum #2=\@ne
       \vskip-\prevdepth \prevdepth\z@ \vskip\Cvs
       \advance\@tempskipa-\Cvs \vspace*{\@tempskipa}%
     \else
      \addvspace\@tempskipa
     \fi
   \fi
 \@ifstar{\@ssect{#3}{#4}{#5}{#6}}{\@dblarg{\@sect{#1}{#2}{#3}{#4}{#5}{#6}}}}


\def\@sect#1#2#3#4#5#6[#7]#8{%
  \ifnum #2>\c@secnumdepth
    \let\@svsec\@empty
  \else
    \refstepcounter{#1}%
%    \protected@edef\@svsec{\fontsize{16\Q}{18H}\selectfont\@seccntformat{#1}\relax}%
    \protected@edef\@svsec{\selectfont\@seccntformat{#1}\relax}%
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
%%%%
 \setbox\@tempboxb\hbox{\large#6{%
      \@hangfrom{%
%\hangindent=\wd\@tempboxa\hangafter=-10
\hskip #3\relax{\csname #2@font\endcsname \@svsec}}}}%\the\wd\@tempboxb
\setbox\SECTwd=\hbox{%
\begingroup\noindent\large%
    #6{%
      \@hangfrom{%
%\hangindent=\wd\@tempboxa\hangafter=-10
\hskip #3\relax{\csname #2@font\endcsname \@svsec}}%★%
       \interlinepenalty \@M %\@secjidori
\shortstack[l]{%
%\noindent\box\@tempboxa
\noindent
#8}\@@par}%
   \endgroup
}
%%%%
  \ifdim \wd\SECTwd > \columnwidth
%    \begingroup
   \noindent%\parbox[t]{\columnwidth}
%\vskip-\prevdepth \prevdepth\z@ \vskip\Cvs
%\advance\@tempskipa-\Cvs 
%\vspace*{\@tempskipa}%
{\begingroup\noindent
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%★2%
          \interlinepenalty \@M 
\noindent\hangindent\wd\@tempboxb\hangafter=1
#8\@@par}%
    \endgroup}
\else
%%%%%%%%%
  \ifdim \ht\SECTht > \baselineskip
   \hfil\parbox[c]{\wd\SECTwd}%
{\begingroup\noindent
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%★3%
          \interlinepenalty \@M 
\noindent\hangindent\wd\@tempboxb\hangafter=1
#8\@@par%\prevdepth\z@
}%
    \endgroup}
\vskip-\prevdepth \prevdepth\z@ %
%\vskip\Cvs
%       \advance\@tempskipa-\Cvs \vspace*{\@tempskipa}%
  \else
%%%%%%%%%
    \noindent\begingroup\noindent\hfil
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%
          \interlinepenalty \@M 
\SEVENjidori{#8}\@@par}%
    \endgroup
\fi\fi%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \csname #1mark\endcsname{#7}%
    \addcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      \protect\SEVENjidori{#7}}%
  \else
    \def\@svsechd{%
      #6{\hskip #3\relax
      \@svsec #8}%
      \csname #1mark\endcsname{#7}%
      \addcontentsline{toc}{#1}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        \protect\SEVENjidori{#7}}}%
  \fi
  \@xsect{#5}}
\def\@xsect#1{%
  \@tempskipa #1\relax
  \ifdim \@tempskipa>\z@
    \par \nobreak
    \vskip \@tempskipa
    \@afterheading
  \else
    \@nobreakfalse
    \global\@noskipsectrue
    \everypar{%
      \if@noskipsec
        \global\@noskipsecfalse
       {\setbox\z@\lastbox}%
        \clubpenalty\@M
        \begingroup \@svsechd \endgroup
        \unskip
        \@tempskipa #1\relax
        \hskip -\@tempskipa
      \else
        \clubpenalty \@clubpenalty
        \everypar{}%
      \fi}%
  \fi
  \ignorespaces}
\def\@seccntformat#1{\csname the#1\endcsname\quad}

\def\@ssect#1#2#3#4#5{%
  \@tempskipa #3\relax
  \ifdim \@tempskipa>\z@
%%%
\setbox\SECTwd=\hbox{%
\begingroup\noindent
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M %
\shortstack[l]{
\noindent
#5}\@@par}%
    \endgroup
}
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  \ifdim \wd\SECTwd > \columnwidth
   \noindent%
{\begingroup
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M 
\noindent%\hangindent\wd\@tempboxb\hangafter=1
#5\@@par}%
    \endgroup}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\else
    \noindent\begingroup\hfil
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M \SEVENjidori{#5}\@@par}%
    \endgroup
\fi
  \else
    \def\@svsechd{#4{\hskip #1\relax #5}}%
  \fi
  \@xsect{#3}}





%%%%% 見出し和文文字はゴシック、欧文はボールド
%%% 節=\section は センタリング
 \newcommand{\section}{\@startsection{section}{1}{0zw}%
   {1\Cvs \@plus.1mm \@minus.1mm}%
   {1\Cvs \@plus.1mm \@minus.1mm}%
   {\reset@font\large%\slshape
%\bfseries%\FutogoXvi%\HelveXvi
%\gt\sffamily
\bfseries
\mathversion{bold}%
%\fontsize{28Q}{32H}\selectfont
}}



 \renewcommand{\section}{\@startsection{section}{1}{0zw}%
   {1\Cvs \@plus.1mm \@minus.5mm}%
   {1\Cvs \@plus.1mm \@minus.1mm}%
   {\reset@font\large%\slshape
%\bfseries%\FutogoXvi%\HelveXvi
%\gt\sffamily
\bfseries
\mathversion{bold}%
%\fontsize{28Q}{32H}\selectfont
}}



%\newcommand{\section}{\@startsection{section}{1}{\z@}%
%   {1.5\Cvs \@plus.5\Cdp \@minus.2\Cdp}%
%   {.5\Cvs \@plus.3\Cdp}%
%   {\reset@font\Large\bfseries}}




%%% \subsection subsubsection 項、目などは左寄
\def\@startsectionB#1#2#3#4#5#6{\if@noskipsec \leavevmode \fi
  \par  \@tempskipa #4\relax
  \@afterindenttrue
  \ifdim \@tempskipa <\z@    \@tempskipa -\@tempskipa \@afterindentfalse  \fi
  \if@nobreak
    \everypar{}%
  \else
    \addpenalty\@secpenalty
\ifnum #2=\@ne
       \vskip-\prevdepth \prevdepth\z@ \vskip\Cvs
       \advance\@tempskipa-\Cvs \vspace*{\@tempskipa}%
     \else
\addvspace\@tempskipa
\fi
  \fi
  \@ifstar
    {\@ssectB{#3}{#4}{#5}{#6}}%
    {\@dblarg{\@sectB{#1}{#2}{#3}{#4}{#5}{#6}}}}

\def\@sectB#1#2#3#4#5#6[#7]#8{%
  \ifnum #2>\c@secnumdepth
    \let\@svsec\@empty
  \else
    \refstepcounter{#1}%
    \protected@edef\@svsec{%\protect\rule{0mm}{21.75mm}
\@seccntformatB{#1}\relax}%
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
   \begingroup
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%
          \interlinepenalty \@M
\protect\SEVENjidori
{#8}\@@par}%
    \endgroup%
    \csname #1mark\endcsname{#7}%
    \addcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      \protect\SEVENjidori{#7}}%
  \else
    \def\@svsechd{%
      #6{\hskip #3\relax
      \@svsec #8}%
      \csname #1mark\endcsname{#7}%
      \addcontentsline{toc}{#1}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        #7}}%
  \fi
  \@xsect{#5}}
\def\@xsect#1{%
  \@tempskipa #1\relax
  \ifdim \@tempskipa>\z@
    \par \nobreak
    \vskip \@tempskipa
    \@afterheading
  \else
    \@nobreakfalse
    \global\@noskipsectrue
    \everypar{%
      \if@noskipsec
        \global\@noskipsecfalse
       {\setbox\z@\lastbox}%
        \clubpenalty0%\@M
        \begingroup \@svsechd \endgroup
        \unskip
        \@tempskipa #1\relax
        \hskip -\@tempskipa
      \else
        \clubpenalty \@clubpenalty
        \everypar{}%
      \fi}%
  \fi
  \ignorespaces}
%\def\@seccntformatA#1{\protect\SECTUP{\csname the#1\endcsname\quad}}
\def\@seccntformatB#1{\csname the#1\endcsname\hskip1zw
}
\def\@ssectB#1#2#3#4#5{%
  \@tempskipa #3\relax
  \ifdim \@tempskipa>\z@
    \begingroup
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M \protect\SEVENjidori{#5}\@@par}%
    \endgroup
  \else
    \def\@svsechd{#4{\hskip #1\relax #5}}%
  \fi
  \@xsect{#3}}
\newif\if@afterindent \@afterindenttrue
\def\@afterheading{%
  \@nobreaktrue
  \everypar{%
    \if@nobreak
      \@nobreakfalse
      \clubpenalty0 %\@M
      \if@afterindent \else
        {\setbox\z@\lastbox}%
      \fi
    \else
      \clubpenalty \@clubpenalty
      \everypar{}%
    \fi}}








\newcommand{\subsection}{\@startsectionB{subsection}{2}{1zw}%
%   {1.5\Cvs \@plus.5\Cdp \@minus.2\Cdp}%
%   {.5\Cvs \@plus.3\Cdp}%
   {1\Cvs \@plus.1mm \@minus.1mm}%
   {.0001mm \@plus.1mm \@minus.1mm}%
   {\reset@font\bfseries}}









%%% \subsubsection 目などは左寄 1行 本文改行なしで2字アキで続ける
\def\@startsectionC#1#2#3#4#5#6{\if@noskipsec \leavevmode \fi
  \par  \@tempskipa #4\relax
  \@afterindenttrue
  \ifdim \@tempskipa <\z@    \@tempskipa -\@tempskipa \@afterindentfalse  \fi
  \if@nobreak
    \everypar{}%
  \else
    \addpenalty\@secpenalty
\ifnum #2=\@ne
       \vskip-\prevdepth \prevdepth\z@ \vskip\Cvs
       \advance\@tempskipa-\Cvs \vspace*{\@tempskipa}%
     \else
\addvspace\@tempskipa
\fi
  \fi
  \@ifstar
    {\@ssectC{#3}{#4}{#5}{#6}}%
    {\@dblarg{\@sectC{#1}{#2}{#3}{#4}{#5}{#6}}}}

\def\@sectC#1#2#3#4#5#6[#7]#8{%
  \ifnum #2>\c@secnumdepth
    \let\@svsec\@empty
  \else
    \refstepcounter{#1}%
    \protected@edef\@svsec{%\protect\rule{0mm}{21.75mm}
\@seccntformatC{#1}\relax}%
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
   \begingroup
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%
          \interlinepenalty \@M
\protect\FIVEjidori
{#8}\@@par}%
    \endgroup%
    \csname  #1mark\endcsname{#7}%
    \addcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      \protect\FIVEjidori{#7}}%
  \else
    \def\@svsechd{%
      #6{\hskip #3\relax
      \@svsec \protect\FIVEjidori{#8}}%
      \csname #1mark\endcsname{#7}%
      \addcontentsline{toc}{#1}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        #7}}%
  \fi
  \@xsectC{#5}}
\def\@xsectC#1{%
  \@tempskipa #1\relax
  \ifdim \@tempskipa>\z@
    \par \nobreak
    \vskip \@tempskipa
    \@afterheading
  \else
    \@nobreakfalse
    \global\@noskipsectrue
    \everypar{%
      \if@noskipsec
        \global\@noskipsecfalse
       {\setbox\z@\lastbox}%
        \clubpenalty0%\@M
        \begingroup \@svsechd \endgroup
        \unskip
        \@tempskipa #1\relax
        \hskip -\@tempskipa
      \else
        \clubpenalty \@clubpenalty
        \everypar{}%
      \fi}%
  \fi
  \ignorespaces}
%% ここで、パーレンにしたいところだが。
%\def\@seccntformatC#1{(\csname the#1\endcsname)\hskip1zw}
\def\@seccntformatC#1{\csname the#1\endcsname\hskip1zw}
\def\@ssectC#1#2#3#4#5{%
  \@tempskipa #3\relax
  \ifdim \@tempskipa>\z@
    \begingroup
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M \protect\FIVEjidori{#5}\@@par}%
    \endgroup
  \else
    \def\@svsechd{#4{\hskip #1\relax #5}}%
  \fi
  \@xsect{#3}}
\newif\if@afterindent \@afterindenttrue
\def\@afterheading{%
  \@nobreaktrue
  \everypar{%
    \if@nobreak
      \@nobreakfalse
      \clubpenalty0 %\@M
      \if@afterindent \else
        {\setbox\z@\lastbox}%
      \fi
    \else
      \clubpenalty \@clubpenalty
      \everypar{}%
    \fi}}






\newcommand{\subsubsection}{\@startsectionC{subsubsection}{3}{1zw}%
%   {-1\Cvs \@plus.5\Cdp \@minus.2\Cdp}%
   {.0001mm \@plus.1mm \@minus.1mm}%
%   {-.0001mm \@plus.1mm \@minus.1mm}%
   {-2zw \@plus.1mm \@minus.1mm}%
%   {.5\Cvs \@plus.3\Cdp}%
   {\reset@font\normalsize\bfseries}}

\newcommand{\paragraph}{\@startsectionC{paragraph}{4}{1zw}%
%   {3.25ex \@plus 1ex \@minus .2ex}%
   {.0001mm \@plus.1mm \@minus.1mm}%
   {-2zw}%
   {\reset@font\normalsize\bfseries}}

\newcommand{\subparagraph}{\@startsection{subparagraph}{5}{\z@}%
   {3.25ex \@plus 1ex \@minus .2ex}%
   {-1em}%
   {\reset@font\normalsize\bfseries}}






%%%%%%%%%%%%%%%%%%% 付録の設定 
%%%% 20Q  中ゴ 7字ﾄﾞﾘ 5行分 天地左右中央

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




\newcommand*{\l@APPsection}{\@dottedtocline{1}{0em}{2.3em}}

\def\@APPsect#1#2#3#4#5#6[#7]#8{%
  \ifnum #2>\c@secnumdepth
    \let\@svsec\@empty
  \else
    \refstepcounter{#1}%
    \protected@edef\@svsec{\@seccntformat{#1}\relax}%
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
%%%%
 \setbox\@tempboxb\hbox{\large#6{%
      \@hangfrom{%
%\hangindent=\wd\@tempboxa\hangafter=-10
\hskip #3\relax{\csname #2@font\endcsname \@svsec}}}}%\the\wd\@tempboxb
\setbox\SECTwd=\hbox{%
\begingroup\noindent\large%
    #6{%
      \@hangfrom{%
%\hangindent=\wd\@tempboxa\hangafter=-10
\hskip #3\relax{\csname #2@font\endcsname \@svsec}}%★%
       \interlinepenalty \@M %\@secjidori
\shortstack[l]{%
%\noindent\box\@tempboxa
\noindent
#8}\@@par}%
   \endgroup
}
%%%%
  \ifdim \wd\SECTwd > \columnwidth
%    \begingroup
   \noindent%\parbox[t]{\columnwidth}
%\vskip-\prevdepth \prevdepth\z@ \vskip\Cvs
%\advance\@tempskipa-\Cvs 
%\vspace*{\@tempskipa}%
{\begingroup\noindent
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%★2%
          \interlinepenalty \@M 
\noindent\hangindent\wd\@tempboxb\hangafter=1
#8\@@par}%
    \endgroup}
\else
%%%%%%%%%
  \ifdim \ht\SECTht > \baselineskip
   \hfil\parbox[c]{\wd\SECTwd}%
{\begingroup\noindent
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%★3%
          \interlinepenalty \@M 
\noindent\hangindent\wd\@tempboxb\hangafter=1
#8\@@par%\prevdepth\z@
}%
    \endgroup}
\vskip-\prevdepth \prevdepth\z@ %
%\vskip\Cvs
%       \advance\@tempskipa-\Cvs \vspace*{\@tempskipa}%
  \else
%%%%%%%%%
    \noindent\begingroup\noindent\hfil
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%
          \interlinepenalty \@M 
\SEVENjidori{#8}\@@par}%
    \endgroup
\fi\fi%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \csname #1mark\endcsname{#7}%
%    \addcontentsline{toc}{#1}{%
    \addcontentsline{toc}{APPsection}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      \protect\SEVENjidori{#7}}%
  \else
    \def\@svsechd{%
      #6{\hskip #3\relax
      \@svsec #8}%
      \csname #1mark\endcsname{#7}%
%      \addcontentsline{toc}{#1}{%
      \addcontentsline{toc}{APPsection}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        \protect\SEVENjidori{#7}}}%
  \fi
  \@xsect{#5}}


%% 
\newcommand{\appendix}{\par
  \setcounter{chapter}{0}%
  \setcounter{section}{0}%
  \setcounter{equation}{0}%
  \setcounter{figure}{0}%
  \setcounter{table}{0}%
  \renewcommand{\@chapapp}{\appendixname}%
  \renewcommand{\@chappos}\space%
  \renewcommand{\thechapter}{\@Alph\c@chapter}
\renewcommand{\thefigure}{%
%\ifnum\c@figure=1
%  \ifnum\c@chapter>\z@ 
%{\bfseries 図\thechapter.\fi\@arabic\c@figure}%
%\else
%  \ifnum\c@chapter>\z@ 図\thechapter.\fi 図\@arabic\c@figure%
  \ifnum\c@chapter>\z@ 図\@Alph\c@chapter.\@arabic\c@figure\else 図\@arabic\c@figure\fi%
%\fi%
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\renewcommand{\thetable}{%
%  \ifnum\c@chapter>\z@ 表\thechapter.\fi 表\@arabic\c@table}
  \ifnum\c@chapter>\z@ 表\@Alph\c@chapter.\@arabic\c@table\else 表\@arabic\c@table\fi}
%  \renewcommand{\thesection}{\@Alph\c@section.}
%  \renewcommand{\thesection}{\ifnum\c@chapter>\z@
%  \thechapter.\@arabic\c@section  \else  A.\c@section\fi}
%\renewcommand{\thesection}{\ifnum\c@chapter<\z@ A \else\thechapter\fi}
%  \renewcommand{\theequation}{(\ifnum\c@section>\z@ \thesection\else
%  \@arabic\c@equation\fi)}%
  \renewcommand{\theequation}{(\thechapter.\@arabic\c@equation)}%
\let\@sect\@APPsect
}




\newenvironment{Appendix}{\appendix%
%\def\@schapter##1{%
\refstepcounter{chapter}%
%  \@makeAPPschapterhead{##1}\@afterheading
%}
%  \if@openright\clearpage\else\clearpage\fi
\chapter*{付録}%
\addtocontents{toc}{\protect\addvspace{5.5mm}}% 直前が項目次のとき、8mm% アキ
\addcontentsline{toc}{TUKIMONOchapter}{付録}%
\addtocontents{toc}{\protect\addvspace{3\h}}%
\thispagestyle{CHAPheadings}
\ifnum \c@section >0
\@mkboth{付録}{\rightmark}\else
\@mkboth{付録}{付録}\fi
%
}{\clearpage}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newdimen\APPSCHAPheight
\APPSCHAPheight=4\baselineskip 
\addtolength{\APPSCHAPheight}{\topskip}%
%
\def\@makeAPPschapterhead#1{\clearpage%
\normalsize\baselineskip25\h%\hbox{}%
\APPSCHAPheight=4\baselineskip 
\addtolength{\APPSCHAPheight}{\topskip}%
\addtolength{\APPSCHAPheight}{4H}%%% 行間12H(13Q25H)-8H(12Q20H)=4H の差
%\the\APPSCHAPheight
\vbox to \APPSCHAPheight
%\vbox to 87.16618pt
  {%\vfill
\vskip2\Cvs\parindent\z@
   \raggedright
   \reset@font\huge\bfseries
   \leavevmode
   \setlength\@tempdima{\linewidth}%
   \centerline{%\hsize\@tempdima
\fontsize{20\JQ}{32H}\selectfont\SEVENjidori{#1}}\par\vfill
%\smash{.\hskip30mm.\hskip40mm.}
}%\vskip3\Cvs
}
%


\renewenvironment{Appendix}{%
%
%
\def\@schapter##1{%
  \@makeAPPschapterhead{##1}%\@afterheading
}

\appendix%
%\def\@schapter##1{%
\refstepcounter{chapter}%
%  \@makeAPPschapterhead{##1}\@afterheading
%}
%  \if@openright\clearpage\else\clearpage\fi
\chapter*{付録}%
\addtocontents{toc}{\protect\addvspace{5.5mm}}% 直前が項目次のとき、8mm% アキ
\addcontentsline{toc}{TUKIMONOchapter}{付録}%
\addtocontents{toc}{\protect\addvspace{3\h}}%
\thispagestyle{CHAPheadings}
\ifnum \c@section >0
\@mkboth{付録}{\rightmark}\else
\@mkboth{付録}{付録}\fi
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 \renewcommand{\section}{\@startsection{section}{1}{0zw}%
   {
\ifnum\c@section<1
0mm \@plus.1mm \@minus3.5mm
\else
1\Cvs \@plus.1mm \@minus.1mm
\fi
}%
   {
\ifnum\c@section=1
0.75\Cvs \@plus.1mm \@minus.1mm
\else
1.125\Cvs \@plus.1mm \@minus.1mm
\fi
}%
   {\reset@font\large%\slshape
%\bfseries%\FutogoXvi%\HelveXvi
%\gt\sffamily
\bfseries
\mathversion{bold}%
%\fontsize{28Q}{32H}\selectfont
}}
\renewcommand{\subsection}{\@startsectionB{subsection}{2}{1zw}%
%   {1.5\Cvs \@plus.5\Cdp \@minus.2\Cdp}%
%   {.5\Cvs \@plus.3\Cdp}%
   {1\Cvs \@plus.1mm \@minus.1mm}%
   {.0001mm \@plus.1mm \@minus.1mm}%
   {\reset@font\small\bfseries\mathversion{bold}}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%$
%
%
\normalsize
\par
\small
}{\clearpage}

%%% 節=\section は センタリング


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%% 章末問題解答

\newcounter{ANSchapter}

%% 
\newcommand{\QandA}{\par
  \setcounter{chapter}{0}%
  \setcounter{section}{0}%
  \setcounter{equation}{0}%
  \setcounter{figure}{0}%
  \setcounter{table}{0}%
%  \renewcommand{\thechapter}{\@Alph\c@chapter}
%  \renewcommand{\thesection}{\@Alph\c@section.}
%  \renewcommand{\thesection}{\ifnum\c@chapter>\z@
%  \thechapter.\@arabic\c@section  \else  A.\c@section\fi}
%\renewcommand{\thesection}{\ifnum\c@chapter<\z@ A \else\thechapter\fi}
%  \renewcommand{\theequation}{(\ifnum\c@section>\z@ \thesection\else
%  \@arabic\c@equation\fi)}%
\@addtoreset{figure}{ANSchapter}
\renewcommand{\thefigure}{%
%\ifnum\c@figure=1
%  \ifnum\c@chapter>\z@ 
%{\bfseries 図\thechapter.\fi\@arabic\c@figure}%
%\else
  \ifnum\c@chapter>\z@ 解図\theANSchapter.\fi\@arabic\c@figure%
%\fi%
}
\@addtoreset{table}{ANSchapter}
\renewcommand{\thetable}{%
  \ifnum\c@chapter>\z@ 解表\theANSchapter.\fi\@arabic\c@table}
\@addtoreset{equation}{ANSchapter}
  \renewcommand{\theequation}{(\@arabic\c@equation)}%
}


\newcounter{ANSchapVAL}

\newcommand{\answer}{\refstepcounter{ANSchapVAL}%
\ifnum\the\value{ANSchapVAL}<2
\else
\vskip1\Cvs
\fi
\par\noindent{%
\refstepcounter{ANSchapter}\normalsize\bfseries \theANSchapter 章}\nopagebreak
}


\newenvironment{Answer}{\QandA%
%
%\leftmargin3zw
%\renewcommand{\labelenumi}{\theenumi}
%\renewcommand{\theenumi}{\<【\@arabic\c@enumi】}
%\def\@schapter##1{%
\refstepcounter{chapter}%
%  \@makeAPPschapterhead{##1}\@afterheading
%}
%  \if@openright\clearpage\else\clearpage\fi
\chapter*{章末問題解答}\addcontentsline{toc}{TUKIMONOchapter}{章末問題解答}%
\addtocontents{toc}{\protect\addvspace{3\h}}%
\thispagestyle{CHAPheadings}
\@mkboth{章末問題解答}{章末問題解答}
%
\let\enumerate=\Senumerate
\bgroup\small}{\egroup\clearpage}



%%%%%%%%%%%%%%%%%%




















%%% list 
\def\list#1#2{%
  \ifnum \@listdepth >5\relax
    \@toodeep
  \else
    \global\advance\@listdepth\@ne
  \fi
  \rightmargin\z@
  \listparindent\z@
  \itemindent\z@
  \csname @list\romannumeral\the\@listdepth\endcsname\topsep0pt
  \def\@itemlabel{#1}%
  \let\makelabel\@mklab
  \@nmbrlistfalse
  #2\relax
  \@trivlist
  \parskip\parsep
  \parindent\listparindent
  \advance\linewidth -\rightmargin
  \advance\linewidth -\leftmargin
  \advance\@totalleftmargin \leftmargin
  \parshape \@ne \@totalleftmargin \linewidth
  \ignorespaces}
















\if@twocolumn
  \setlength\leftmargini {2em}
\else
  \setlength\leftmargini {2.5em}
\fi
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\if@twocolumn
  \setlength\leftmarginv {.5em}
  \setlength\leftmarginvi{.5em}
\else
  \setlength\leftmarginv {1em}
  \setlength\leftmarginvi{1em}
\fi
\setlength  \labelsep  {.5em}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
\renewcommand{\theenumi}{\@arabic\c@enumi}
\renewcommand{\theenumii}{\@alph\c@enumii}
\renewcommand{\theenumiii}{\@roman\c@enumiii}
\renewcommand{\theenumiv}{\@Alph\c@enumiv}
\newcommand{\labelenumi}{\theenumi.}
\newcommand{\labelenumii}{(\theenumii)}
\newcommand{\labelenumiii}{\theenumiii.}
\newcommand{\labelenumiv}{\theenumiv.}
\renewcommand{\p@enumii}{\theenumi}
\renewcommand{\p@enumiii}{\theenumi(\theenumii)}
\renewcommand{\p@enumiv}{\p@enumiii\theenumiii}


\renewenvironment{enumerate}
  {\ifnum \@enumdepth >\thr@@\@toodeep\else
   \advance\@enumdepth\@ne
   \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
   \list{\csname label\@enumctr\endcsname}{%
      \iftdir
         \ifnum \@listdepth=\@ne \topsep.5\normalbaselineskip
           \else\topsep\z@\fi
         \parskip\z@ \itemsep\z@ \parsep\z@
         \labelwidth1zw \labelsep.3zw
         \ifnum \@enumdepth=\@ne \leftmargin1zw\relax
           \else\leftmargin\leftskip\fi
         \advance\leftmargin 1zw
      \fi
         \usecounter{\@enumctr}%
         \def\makelabel##1{\hss\llap{##1}}}%
   \fi}{\endlist}


%%%% 1. 2. ....
\renewenvironment{enumerate}
  {%% <
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
%     \leftmargin2zw%\z@
     \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
%     \itemindent1zw
%     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
     \def\makelabel##1{\hss\llap{##1}}}%
    \fi}{\endlist}


%%%% a. b. ....
\newenvironment{enumerateA}
  {%% <
%  {\renewcommand{\labelenumi}{(\theenumi)}%% <
\renewcommand{\theenumi}{\@alph\c@enumi}
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
     \leftmargin2zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent1zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
     \def\makelabel##1{\hss\llap{##1}}}%
    \fi}{\endlist}





%%%% (1), (2), (3),....
\newenvironment{Arabicenumerate}
  {\renewcommand{\labelenumi}{(\theenumi)}%
%% <
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
     \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent-0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
     \def\makelabel##1{\hss\llap{##1}}}%
    \fi}{\endlist}






%%%% 1), 2), 3),....
\newenvironment{arabicenumerate}
  {\renewcommand{\labelenumi}{\theenumi)}%
%% <
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
     \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent-0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
     \def\makelabel##1{\hss\llap{##1}}}%
    \fi}{\endlist}








%%%% (a), (b), (c),....
\newenvironment{Alphenumerate}
  {\renewcommand{\labelenumi}{(\theenumi)}%% <
\renewcommand{\theenumi}{\@alph\c@enumi}
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
     \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent-0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
     \def\makelabel##1{\hss\llap{##1}}}%
    \fi}{\endlist}

%%%% a), b), c),....
\newenvironment{alphenumerate}
  {\renewcommand{\labelenumi}{\theenumi)}%% <
\renewcommand{\theenumi}{\@alph\c@enumi}
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
     \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent-0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
     \def\makelabel##1{\hss\llap{##1}}}%
    \fi}{\endlist}




%%%% (i), (ii), (iii),....
\newenvironment{Romanenumerate}
  {\renewcommand{\labelenumi}{(\theenumi)}%% <
\renewcommand{\theenumi}{\@roman\c@enumi}
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
     \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent-0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
     \def\makelabel##1{\hss\llap{##1}}}%
    \fi}{\endlist}


%%%% i), ii), iii),....
\newenvironment{romanenumerate}
  {\renewcommand{\labelenumi}{\theenumi)}%% <
\renewcommand{\theenumi}{\@roman\c@enumi}
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
     \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent-0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
     \def\makelabel##1{\hss\llap{##1}}}%
    \fi}{\endlist}








%%%%%%%%%%%%%%%% Sample.tex p.20の箇条書の例のための
%% \begin{箇条書}...仮の環境名
% (1) ......
%   (a).....
% (2) ......

\newenvironment{箇条書}
  {%% <
%\ifnum \theenumi %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%
%\renewcommand{\labelenumi}{\theenumi..}
%   \ifnum \@enumdepth >3\relax\@toodeep\else
   \ifnum \@enumdepth =2\relax\@toodeep\else
\ifnum %\theenumi
\@enumdepth=0
%%%
\renewcommand{\labelenumi}{\theenumi}
\renewcommand{\theenumi}{(\@arabic\c@enumi)}
%%
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
%\renewcommand{\theenumi}{(\@arabic\c@enumi)}
%{\<【\hbox to10.64987pt{\hfill{\bfseries\@arabic\c@enumi}\hfill}】\<}
     \leftmargin2zw%27.72026pt%
     \labelwidth2zw%19.18506pt%
     \labelsep0.25zw%1zw
     \itemindent1zw%0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}}}
\else
\ifnum %\theenumi
\@enumdepth=1
\renewcommand{\labelenumii}{\theenumii}
\renewcommand{\theenumii}{(\@alph\c@enumii)}
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
   \list{\csname label\@enumctr\endcsname}{%
%
     \leftmargin0zw%\z@
     \labelwidth2zw%0zw
     \labelsep0.25zw%.75zw
     \itemindent1zw%-1.375zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}\hss}}
\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
   \list{\csname label\@enumctr\endcsname}{%
     \leftmargin12zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent1zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}}}
\fi\fi
%
\fi%
%
%%%%%%%%%%%%%%%%%%%%%%%%%
}{\endlist}


%% \begin{手順}...仮の環境名
% 1) ......
%   a).....
% 2) ......

\newenvironment{手順}
  {%% <
%\ifnum \theenumi %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%
%\renewcommand{\labelenumi}{\theenumi..}
%   \ifnum \@enumdepth >3\relax\@toodeep\else
   \ifnum \@enumdepth =2\relax\@toodeep\else
\ifnum %\theenumi
\@enumdepth=0
%%%
\renewcommand{\labelenumi}{\theenumi}
\renewcommand{\theenumi}{\@arabic\c@enumi)}
%%
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
%\renewcommand{\theenumi}{(\@arabic\c@enumi)}
%{\<【\hbox to10.64987pt{\hfill{\bfseries\@arabic\c@enumi}\hfill}】\<}
     \leftmargin2zw%27.72026pt%
     \labelwidth1.5zw%19.18506pt%
     \labelsep.25zw
     \itemindent1zw%0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}}}
\else
\ifnum %\theenumi
\@enumdepth=1
\renewcommand{\labelenumii}{\theenumii}
\renewcommand{\theenumii}{\@alph\c@enumii)}
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
   \list{\csname label\@enumctr\endcsname}{%
%
     \leftmargin0zw%\z@
     \labelwidth1.5zw%0zw
     \labelsep.25zw%.75zw
     \itemindent1zw%-1.375zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}\hss}}
\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
   \list{\csname label\@enumctr\endcsname}{%
     \leftmargin12zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent1zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}}}
\fi\fi
%
\fi%
%
%%%%%%%%%%%%%%%%%%%%%%%%%
}{\endlist}










%%%% 章末問題の箇条書の設定 Senumerate 
\newenvironment{Senumerate}
  {%% <
%\ifnum \theenumi %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%
%\renewcommand{\labelenumi}{\theenumi..}
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
\ifnum \theenumi=2
\renewcommand{\labelenumi}{\theenumi}
     \leftmargin2.625zw%\z@
     \labelwidth0zw
     \labelsep1zw
     \itemindent-1.625zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
%    \def\makelabel##1{【{\bfseries##1】}}
    \def\makelabel##1{\hbox to2zw{\<【\hfill\bfseries##1\hfill】\<}}
\else
\ifnum \@enumdepth=3

%\renewcommand{\labelenumii}{\theenumii}
     \leftmargin2zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent1zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}}
\else
     \leftmargin12zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent1zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}}
\fi\fi
}%
\fi%
%
%%%%%%%%%%%%%%%%%%%%%%%%%
}{\endlist}










%%% 章末問題の箇条書の設定 Senumerate 
\renewenvironment{Senumerate}
  {%% <
%\ifnum \theenumi %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%
%\renewcommand{\labelenumi}{\theenumi..}
%   \ifnum \@enumdepth >3\relax\@toodeep\else
   \ifnum \@enumdepth =2\relax\@toodeep\else
\ifnum %\theenumi
\@enumdepth=0
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
\renewcommand{\labelenumi}{\theenumi}
%     \leftmargin2.625zw%\z@
     \leftmargin27.72026pt%0zw%\z@
     \labelwidth19.18506pt%0zw
     \labelsep1zw
%     \itemindent-1.625zw
     \itemindent0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
%    \def\makelabel##1{\<【\hbox to10.64987pt{\hfill{\bfseries##1\hfill}】
%\<%\hfill
%}}}
    \def\makelabel##1{\<【\hbox to10.64987pt{\hfill{\bfseries##1}\hfill}】\<}}
\else
\ifnum %\theenumi
\@enumdepth=1
\renewcommand{\labelenumii}{(\theenumii)}
\renewcommand{\theenumii}{\@arabic\c@enumii}
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
   \list{\csname label\@enumctr\endcsname}{%
%
     \leftmargin2zw%\z@
     \labelwidth0zw
     \labelsep.75zw
     \itemindent-1.375zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}\hss}}
\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
   \list{\csname label\@enumctr\endcsname}{%
     \leftmargin12zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent1zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}}}
\fi\fi
%
\fi%
%
%%%%%%%%%%%%%%%%%%%%%%%%%
}{\endlist}








%%% last
%%% 章末問題の箇条書の設定 Senumerate 
\renewenvironment{Senumerate}
  {%% <
%\ifnum \theenumi %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%
%\renewcommand{\labelenumi}{\theenumi..}
%   \ifnum \@enumdepth >3\relax\@toodeep\else
   \ifnum \@enumdepth =2\relax\@toodeep\else
\ifnum %\theenumi
\@enumdepth=0
%%%
\renewcommand{\labelenumi}{\theenumi}
%\renewcommand{\theenumi}{(\@arabic\c@enumi)}
%%
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
\renewcommand{\theenumi}%{\@arabic\c@enumi}
{\<【\hbox to10.64987pt{\hfill{\bfseries\@arabic\c@enumi}\hfill}】\<}
     \leftmargin27.72026pt%0zw%\z@
     \labelwidth19.18506pt%0zw
     \labelsep1zw
     \itemindent0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{\bfseries##1}}}
\else
\ifnum %\theenumi
\@enumdepth=1
\renewcommand{\labelenumii}{\theenumii}
\renewcommand{\theenumii}{(\@arabic\c@enumii)}
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
   \list{\csname label\@enumctr\endcsname}{%
%
     \leftmargin2zw%\z@
     \labelwidth0zw
     \labelsep.75zw
     \itemindent-1.375zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}\hss}}
\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
   \list{\csname label\@enumctr\endcsname}{%
     \leftmargin12zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent1zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
    \def\makelabel##1{{##1}}}
\fi\fi
%
\fi%
%
%%%%%%%%%%%%%%%%%%%%%%%%%
}{\endlist}












\newenvironment{章末問題}{\normalsize%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%\let\enumerate=\Senumerate
\renewenvironment{enumerate}{\begin{Senumerate}}{\end{Senumerate}}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section*{章末問題}\markright{章末問題}%%% 10/31
\addcontentsline{toc}{section}{\mokuSEVENjidori{章末問題}}
\bgroup\small%
\begin{enumerate}
}
{%
\end{enumerate}%\endlist
\egroup\normalsize}







\newcommand{\labelitemi}{\textbullet}
\newcommand{\labelitemii}{%
  \iftdir
     {\textcircled{~}}
  \else
     {\normalfont\bfseries\textendash}
  \fi
}
\newcommand{\labelitemiii}{\textasteriskcentered}
\newcommand{\labelitemiv}{\textperiodcentered}




\newenvironment{AAAAromanenumerate}
  {\renewcommand{\labelenumi}{\theenumi)}%% <
\renewcommand{\theenumi}{\@roman\c@enumi}
   \ifnum \@enumdepth >3\relax\@toodeep\else
    \advance\@enumdepth\@ne
    \edef\@enumctr{enum\romannumeral\the\@enumdepth}%
    \list{\csname label\@enumctr\endcsname}{%
     \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent-0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
     \clubpenalty-200
     \usecounter{\@enumctr}%
     \def\makelabel##1{\hss\llap{##1}}}%
    \fi}{\endlist}




\renewenvironment{itemize}
  {\ifnum \@itemdepth >\thr@@\@toodeep\else
   \advance\@itemdepth\@ne
   \edef\@itemitem{labelitem\romannumeral\the\@itemdepth}%
   \expandafter
   \list{\csname \@itemitem\endcsname}{%
    \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent-0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
      \iftdir
         \ifnum \@listdepth=\@ne \topsep.5\normalbaselineskip
           \else\topsep\z@\fi
%         \parskip\z@ \itemsep\z@ \parsep\z@
%         \labelwidth1zw \labelsep.3zw
    \leftmargin3zw%\z@
     \labelwidth2zw
     \labelsep1zw
     \itemindent-0zw
     \listparindent1zw
     \topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
         \ifnum \@itemdepth =\@ne \leftmargin1zw\relax
           \else\leftmargin\leftskip\fi
         \advance\leftmargin 1zw
      \fi
         \def\makelabel##1{\hss\llap{##1}}}%
   \fi}{\endlist}


\newenvironment{description}
  {\list{}{\labelwidth\z@ \itemindent-\leftmargin
   \iftdir
     \leftmargin\leftskip \advance\leftmargin3\Cwd
     \rightmargin\rightskip
     \labelsep=1zw \itemsep\z@
     \listparindent\z@ \topskip\z@ \parskip\z@ \partopsep\z@
   \fi
           \let\makelabel\descriptionlabel}}{\endlist}
\newcommand{\descriptionlabel}[1]{%
   \hspace\labelsep\normalfont\bfseries #1}
\newenvironment{verse}
  {\let\\\@centercr
   \list{}{\itemsep\z@ \itemindent -1.5em%
           \listparindent\itemindent
           \rightmargin\leftmargin \advance\leftmargin 1.5em}%
           \item\relax}{\endlist}
\newenvironment{quotation}
  {\list{}{\listparindent 1.5em%
           \itemindent\listparindent
           \rightmargin\leftmargin
           \parsep\z@ \@plus\p@}%
           \item\relax}{\endlist}
\newenvironment{quote}
  {\list{}{\rightmargin\leftmargin}%
           \item\relax}{\endlist}


%%%%% from latex.ltx
\def \@floatboxreset {%
        \reset@font
        \footnotesize\baselineskip15\h%%%=10Q
        \@setminipage
}







\def\G@refundefinedtrue{%
  \gdef\@refundefined{%
    \@latex@warning@no@line{There were undefined references}}}
\let\@refundefined\relax

\def\@FIGsetref#1#2#3{%
  \ifx#1\relax
   \protect\G@refundefinedtrue
   \nfss@text{\reset@font\bfseries ??}%
   \@latex@warning{Reference `#3' on page \thepage \space
             undefined}%
  \else
   \expandafter#2#1\null
  \fi}


\newcount\FIGNUMcnt
\FIGNUMcnt=0

\def\FIGNUM#1{\advance\FIGNUMcnt by \@ne
%                \expandafter
%\def
\ifnum \the\FIGNUMcnt =1
{\bf\csname MYref\the\FIGNUMcnt\endcsname{#1}}% 
\else
\csname MYref\the\FIGNUMcnt\endcsname{#1}%
\fi
}


%\def\FIGref#1{%
%\FIGNUM{%
%\expandafter\@FIGsetref\csname r@#1\endcsname\@firstoftwo{#1}%
%}%
%}

\def\FIGref#1{%
\FIGNUM{%
\expandafter\@FIGsetref\csname r@#1\endcsname\@firstoftwo{#1}%
}%
}



%%% table の相互参照
\def\@TABsetref#1#2#3{%
  \ifx#1\relax
   \protect\G@refundefinedtrue
   \nfss@text{\reset@font\bfseries ??}%
   \@latex@warning{Reference `#3' on page \thepage \space
             undefined}%
  \else
   \expandafter#2#1\null
  \fi}


\newcount\TABNUMcnt
\TABNUMcnt=0

\def\TABNUM#1{\advance\TABNUMcnt by \@ne
%                \expandafter
%\def
\ifnum \the\TABNUMcnt =1
{\bf\csname MYtabref\the\TABNUMcnt\endcsname{#1}}% 
\else
\csname MYtabref\the\TABNUMcnt\endcsname{#1}%
\fi
}


\def\TABref#1{%
\TABNUM{%
\expandafter\@TABsetref\csname r@#1\endcsname\@firstoftwo{#1}%
}%
}





%%%% 
\def\FIGref{\fref@ref{}}
\def\TABref{\fref@ref{}}
%%%% section のレフをボールド
\def\SECref#1{{\bfseries(\ref{#1})}}


% Copyright (C) 1995,1996,1997,1998,1999,2000,2001
%			by Hiroshi Nakashima, Yasuki Saito ands
%                          The Editorial Board of the IPSJ Journal
\def\fref@ref#1{\@ifstar{\fref@sref{#1}}{\fref@iref\bf{#1}}}

\def\fref@iref#1#2#3{{\@ifundefined{fref@r@#3}%
	{#1#2\fref@doref{#3}\global\@namedef{fref@r@#3}{}}{#2\fref@doref{#3}}}}
\def\fref@sref#1#2{#1\fref@doref{#2}}
\def\fref@doref#1{{\let\null\relax\ref{#1}}}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




\newcounter{figure}[chapter]
\renewcommand{\thefigure}{%
%\ifnum\c@figure=1
%  \ifnum\c@chapter>\z@ 
%{\bfseries 図\thechapter.\fi\@arabic\c@figure}%
%\else
%  \ifnum\c@chapter>\z@ 図\thechapter.\fi 図\@arabic\c@figure%
  \ifnum\c@chapter>\z@ 図\@arabic\c@chapter.\@arabic\c@figure\else 図\@arabic\c@figure\fi%
%\fi%
}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}
\def\fnum@figure{%\figurename~
\thefigure}


%%% 図とキャプション のアキ3mm
\newenvironment{figure}
               {\abovecaptionskip1.25mm\belowcaptionskip\z@\let\center=\Center\@float{figure}}
               {\end@float}
\newenvironment{figure*}
               {\@dblfloat{figure}}
               {\end@dblfloat}


%%%%%%% COFFEE ブレーク用のfigur

\newcounter{COFFfigure}
\renewcommand{\theCOFFfigure}{%
%\ifnum\c@figure=1
%  \ifnum\c@chapter>\z@ 
%{\bfseries 図\thechapter.\fi\@arabic\c@figure}%
%\else
%  \ifnum\c@chapter>\z@ 図\thechapter.\fi 図\@arabic\c@figure%
図\@arabic\c@COFFfigure
%\fi%
}
\def\fps@COFFfigure{tbp}
\def\ftype@COFFfigure{3}
\def\ext@COFFfigure{lof}
\def\fnum@COFFfigure{\theCOFFfigure}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\@COFFfloat#1{%
  \@ifnextchar[%
    {\@xfloat{#1}}%
    {\edef\reserved@a{\noexpand\@xfloat{#1}[\csname fps@#1\endcsname]}%
     \reserved@a}}




\def\end@COFFfloat{%
  \@endfloatbox
  \ifnum\@floatpenalty <\z@
    \@largefloatcheck
    \@cons\@currlist\@currbox
    \ifnum\@floatpenalty <-\@Mii
      \penalty -\@Miv
      \@tempdima\prevdepth
      \vbox{}%
      \prevdepth\@tempdima
      \penalty\@floatpenalty
    \else
      \vadjust{\penalty -\@Miv \vbox{}\penalty\@floatpenalty}\@Esphack
    \fi
  \fi
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%% 図とキャプション のアキ3mm
\newenvironment{COFFfigure}
               {\abovecaptionskip1.25mm\belowcaptionskip\z@\let\center=\Center\@COFFfloat{COFFfigure}}
               {\end@COFFfloat}
%%%%%%%

%\renewenvironment{COFFfigure}
%               {\abovecaptionskip1.25mm\belowcaptionskip\z@\let\center=\Center\@float{COFFfigure}}
%               {\end@float}
%%%%%%%




\newcounter{table}[chapter]
\renewcommand{\thetable}{%
%  \ifnum\c@chapter>\z@ 表\thechapter.\fi 表\@arabic\c@table}
  \ifnum\c@chapter>\z@ 表\@arabic\c@chapter.\@arabic\c@table\else 表\@arabic\c@table\fi}

\def\fps@table{tbp}
\def\ftype@table{2}
\def\ext@table{lot}
\def\fnum@table{%\tablename~
\thetable}

%%% 表はキャプションと表のアキ 3mm
\newenvironment{table}
               {%\let\footnote\footnote@tab
\abovecaptionskip\z@\belowcaptionskip2.5mm
\let\center=\Center\@float{table}}
               {\end@float}
\newenvironment{table*}
               {%\let\footnote\footnote@tab
\@dblfloat{table}}
               {\end@dblfloat}

%%%%%%%%%%%%%%% COFFEE ブレーク用の表のカウンタ


\newcounter{COFFtable}
\renewcommand{\theCOFFtable}{表\@arabic\c@COFFtable}

\def\fps@COFFtable{tbp}
\def\ftype@COFFtable{4}
\def\ext@COFFtable{lot}
\def\fnum@COFFtable{\theCOFFtable}

%%% 表はキャプションと表のアキ 3mm
\newenvironment{COFFtable}
               {%\let\footnote\footnote@tab
\abovecaptionskip\z@\belowcaptionskip2.5mm
\let\center=\Center\@COFFfloat{COFFtable}}
               {\end@COFFfloat}

%%%%%%%%%%%%%%%COFFEE ブレーク用の表のカウンタ 了







\newlength\abovecaptionskip
\newlength\belowcaptionskip
%\setlength\abovecaptionskip{10\p@}
%\setlength\belowcaptionskip{0\p@}




\newdimen\capwidth
\capwidth24zw%★ とりあえず 11Q X 24zwしておきます


%%%%%%%%%%%%マクロの本体はここから

{\footnotesize\global\capwidth=24zw}%


%%% 図説 表説の長さを変えるためのスイッチング
\def\caption{%
\@ifnextchar<{\special@caption}{\normal@caption}%
}%



\define@key{corona}{capwidth}{\capwidth=#1}




\newdimen\ycapsep
\ycapsep=3.25mm%% 11Q 2字空き
\define@key{corona}{ycapsep}{\ycapsep=#1}






\newif\if@hang\@hangtrue
\define@key{corona}{hang}[true]{\csname @hang#1\endcsname}


\newif\if@hangalign\@hangalignfalse
\define@key{corona}{hangalign}[true]{\csname @hangalign#1\endcsname}


\def\@true{true}
\def\@false{false}
\define@key{corona}{nohang}[true]{%
   \def\temp@arg{#1}%
   \ifx\temp@arg\@true
      \@hangfalse
   \else
      \@hangtrue
   \fi}%



\newif\if@yoko\@yokofalse
\define@key{corona}{yoko}[true]{\csname @yoko#1\endcsname}

\let\par@or@relax\par



\def\normal@caption{%
   \ifx\@captype\@undefined
     \@latex@error{\noexpand\caption outside float}\@ehd
     \expandafter\@gobble
   \else
     \refstepcounter\@captype
     \expandafter\@firstofone
   \fi
   {\@dblarg{\@caption\@captype}}%
}



\def\special@caption<#1>{%
   \setkeys{corona}{#1}%
%%%%%%%%%%
   \if@yoko
      \let\@makecaption\@Ymakecaption
      \let\par@or@relax
   \fi
%%%%%%%%%%
   \ifx\@captype\@undefined
     \@latex@error{\noexpand\caption outside float}\@ehd
     \expandafter\@gobble
   \else
     \refstepcounter\@captype
     \expandafter\@firstofone
   \fi
   {\@dblarg{\@caption\@captype}}%
}



\long\def\@caption#1[#2]#3{%
  \par@or@relax
  \addcontentsline{\csname ext@#1\endcsname}{#1}%
    {\protect\numberline{\csname the#1\endcsname}{\ignorespaces #2}}%
  \begingroup
  \if@yoko\else
    \@parboxrestore
    \if@minipage
      \@setminipage
    \fi
  \fi
    \normalsize
    \@makecaption{\csname fnum@#1\endcsname}{\ignorespaces #3}\par
  \endgroup}








%%%%%%%%%%%%%%%%%%%%%%%%%%%%%ここまでcaptionの改造


\long\def\@makecaption#1#2{\footnotesize\baselineskip15\h%
\vskip\abovecaptionskip 
 \setbox\@tempboxa\hbox{{\bfseries#1}\hskip1zw\shortstack[l]{#2}}%
 \@tempdima\ht\@tempboxa \advance \@tempdima \dp\@tempboxa
\if@hangalign
 \setbox\@tempboxb\hbox{{\bfseries#1}\hskip1zw}%% <<
\else
\setbox\@tempboxb\hbox{{\bfseries □}}%% <<
\fi
\addtolength{\capwidth}{\wd\@tempboxb}
%%%%%%%
\if@hang
\let\hang@or@not\hangindent
\else
\def\hang@or@not##1##2{}%
\fi
%%%%%%%
 \ifdim \@tempdima > \baselineskip%%2行以上の場合
  \ifdim \wd\@tempboxa > \capwidth
   \hfil\parbox[t]{\capwidth}{\hang@or@not\wd\@tempboxb 
    {\bfseries#1}\hskip1zw #2}%\vskip2\@Q
  \else
   \hfil\parbox[t]{\wd\@tempboxa}{\hang@or@not\wd\@tempboxb 
    {\bfseries#1}\hskip1zw #2}%\vskip2\@Q
  \fi
 \else %% 1行の場合
  \ifdim \wd\@tempboxa > \capwidth %%行幅が長すぎる場合
   \hfil\parbox[t]{\capwidth}{\hang@or@not\wd\@tempboxb 
    {\bfseries#1}\hskip1zw #2}\hfil
  \else
   \setbox\@tempboxb\hbox{#2}%
   \ifdim \wd\@tempboxb < 4.5zw %% >
    \hbox to\hsize{\hfil{\bfseries#1}\hskip1zw#2\hfil}
   \else
    \hbox to\hsize{\hfil\box\@tempboxa\hfil}
   \fi
  \fi
 \fi
\vskip\belowcaptionskip
}




\long\def\@Ymakecaption#1#2{\hspace*{\ycapsep}%{3.5mm}
\footnotesize\baselineskip15\h%
\belowcaptionskip3.25mm%% (3mm上に)
 \setbox\@tempboxa\hbox{{\bfseries#1}\hskip1zw\shortstack[l]{#2}}%
 \@tempdima\ht\@tempboxa \advance \@tempdima \dp\@tempboxa
\if@hangalign
 \setbox\@tempboxb\hbox{{\bfseries#1}\hskip1zw}%% <<
\else
\setbox\@tempboxb\hbox{{\bfseries □}}%% <<
\fi
\addtolength{\capwidth}{\wd\@tempboxb}
%%%%%%%%
\if@hang
\let\hang@or@not\hangindent
\else
\def\hang@or@not##1##2{}%
\fi
%%
%\if@hangalign
%\let\hang@or@not\hangindent
%\let\@tempboxb\@tempboxc
%\else
%\def\hang@or@not##1##2{}%
%\fi
%%%%%%%%
 \ifdim \@tempdima > \baselineskip
  \ifdim \wd\@tempboxa > \capwidth
%   \hfil
\parbox[b]{\capwidth}{\hang@or@not\wd\@tempboxb 
    {\bfseries#1}\hskip1zw #2\vskip\belowcaptionskip}%\vskip2\@Q
  \else
%   \hfil
\parbox[b]{\wd\@tempboxa}{\hang@or@notindent\wd\@tempboxb 
    {\bfseries#1}\hskip1zw #2\vskip\belowcaptionskip}%\vskip2\@Q
  \fi
 \else %% <
  \ifdim \wd\@tempboxa > \capwidth
%   \hfil
\parbox[b]{\capwidth}{\hang@or@not\wd\@tempboxb 
    {\bfseries#1}\hskip1zw #2\vskip\belowcaptionskip}
  \else
   \setbox\@tempboxb\hbox{#2}%
   \ifdim \wd\@tempboxb < 4.5zw %% >
\raisebox{\belowcaptionskip}{%\hfil
{\bfseries#1}\hskip1zw#2%\hfil
}
   \else
\raisebox{\belowcaptionskip}{%\hfil
\box\@tempboxa%\hfil
}
   \fi
  \fi
 \fi
}



%%%% 図表を横に並べるための、改造 begin

\long\def\@YOKOcaption#1[#2]#3{%
  \par@or@relax
  \addcontentsline{\csname ext@#1\endcsname}{#1}%
    {\protect\numberline{\csname the#1\endcsname}{\ignorespaces #2}}%
  \begingroup
  \if@yoko\else
    \@parboxrestore
    \if@minipage
      \@setminipage
    \fi
  \fi
    \normalsize
    \@makecaption{\csname fnum@#1\endcsname}{\ignorespaces #3}%\par
  \endgroup}





\long\def\@makeYOKOcaption#1#2{\footnotesize\baselineskip15\h%
%\capwidth=\wd\@tempboxa
%\vskip\abovecaptionskip
 \setbox\@tempboxa\hbox{{\bfseries#1}\hskip1zw\shortstack[l]{#2}}%
 \@tempdima\ht\@tempboxa \advance \@tempdima \dp\@tempboxa
\if@hangalign
 \setbox\@tempboxb\hbox{{\bfseries#1}\hskip1zw}%% <<
\else
\setbox\@tempboxb\hbox{{\bfseries □}}%% <<
\fi
\addtolength{\capwidth}{\wd\@tempboxb}
%%%%%%%
\if@hang
\let\hang@or@not\hangindent
\else
\def\hang@or@not##1##2{}%
\fi
%%%%%%%
 \ifdim \@tempdima > \baselineskip%%2行以上の場合
  \ifdim \wd\@tempboxa > \capwidth
%   \hfil\parbox[t]{\capwidth}{\hang@or@not\wd\@tempboxb
   \hfil\parbox[t]{\wd\@tempboxa}{\hang@or@not\wd\@tempboxb
    {\bfseries#1}\hskip1zw #2}%\vskip2\@Q
  \else
   \hfil\parbox[t]{\wd\@tempboxa}{\hang@or@not\wd\@tempboxb
    {\bfseries#1}\hskip1zw #2}%\vskip2\@Q
  \fi
 \else %% 1行の場合
  \ifdim \wd\@tempboxa > \capwidth %%行幅が長すぎる場合
%   \hfil\parbox[t]{\capwidth}{\hang@or@not\wd\@tempboxb
   \hfil\parbox[t]{\wd\@tempboxa}{\hang@or@not\wd\@tempboxb
    {\bfseries#1}\hskip1zw #2}\hfil
  \else
   \setbox\@tempboxb\hbox{#2}%
   \ifdim \wd\@tempboxb < 4.5zw %% >
%    \hbox to\hsize{\hfil{\bfseries#1}\hskip1zw#2\hfil}
    \hbox to\wd\@tempboxa{\hfil{\bfseries#1}\hskip1zw#2\hfil}
   \else
%    \hbox to\hsize{\hfil\box\@tempboxa\hfil}
    \hbox to\wd\@tempboxa{\hfil\box\@tempboxa\hfil}
   \fi
  \fi
 \fi
%\vskip\belowcaptionskip
}


\newenvironment{Hfloat}{\bgroup\let\@caption\@YOKOcaption\let\@makecaption\@makeYOKOcaption}{\egroup}



%%%% 図表を横に並べるための、改造 end






\setlength\arraycolsep{5\p@}
\setlength\tabcolsep{6\p@}
\setlength\arrayrulewidth{.12mm}
\setlength\doublerulesep{2\p@}
\setlength\tabbingsep{\labelsep}
\skip\@mpfootins = \skip\footins
\setlength\fboxsep{3\p@}
\setlength\fboxrule{.12mm}

\@addtoreset{equation}{chapter}
\renewcommand{\theequation}{%
(\ifnum\c@chapter>\z@\thechapter.\fi \@arabic\c@equation)}




%%%%%% subequationsをamsmath.styのあるなし問わず、使えるようにする
\newcounter{Mparentequation}% Counter for ``parent equation''. by
			    % Matsu

\newenvironment{Msubequations}{%
\renewcommand{\theequation}{%
\ifnum\c@chapter>\z@\thechapter.\fi \@arabic\c@equation}
  \refstepcounter{equation}%
  \protected@edef\theMparentequation{\theequation}%
  \setcounter{Mparentequation}{\value{equation}}%
  \setcounter{equation}{0}%
  \def\theequation{(\theMparentequation\alph{equation})}%
  \ignorespaces
}{%
  \setcounter{equation}{\value{Mparentequation}}%
  \ignorespacesafterend
}




%%%%%%%%%%% COFFEEブレーク用


%%%%%%%%%%%




\newdimen\mathindent
\AtEndOfClass{\mathindent3zw}


%% 数式番号をamsmathを呼んでも上書きされないようにする

\AtBeginDocument{%
\def\tagform@#1{%\maketag@@@{\ignorespaces#1\unskip\@@italiccorr}\quad
{\normalfont \normalcolor {\theequation}\quad}}%
\def\@eqnnum{{\normalfont \normalcolor {\theequation}\quad}}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%\let\parentequation\Mparentequation
%\let\subequations\Msubequations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\everymath={\displaystyle\def\={\,\,=\,\,}}%
%%\everymath={\def\={\,\,=\,\,}}
\everydisplay={\def\={\,\,=\,\,}}
\let\frac=\dfrac
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\@COFFeqnnum{{\normalfont \normalcolor {\theCOFFequation}\quad}}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\COFFtagform@#1{%\maketag@@@{\ignorespaces#1\unskip\@@italiccorr}\quad
{\normalfont \normalcolor {\theCOFFequation}\quad}}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewenvironment{equation}%
    {\@beginparpenalty\predisplaypenalty
     \@endparpenalty\postdisplaypenalty
     \refstepcounter{equation}%
     \parsep  4\p@ \@plus2\p@ \@minus\p@
     \topsep  8\p@ \@plus2\p@ \@minus4\p@
     \itemsep 4\p@ \@plus2\p@ \@minus\p@
     \trivlist \item[]\leavevmode
       \hb@xt@\linewidth\bgroup $\m@th% $
         \displaystyle
         \hskip\mathindent}%
        {$\hfil % $
         \displaywidth\linewidth\hbox{\@eqnnum}%
       \egroup
     \endtrivlist}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5

\@ifundefined{subequations}{
%%%%
\newcounter{parentequation}% Counter for ``parent equation''.
\@ifundefined{ignorespacesafterend}{%
  \def\ignorespacesafterend{\global\@ignoretrue}%
}{}
\newenvironment{subequations}{%
\renewcommand{\theequation}{%
\ifnum\c@chapter>\z@\thechapter.\fi \@arabic\c@equation}
  \refstepcounter{equation}%
  \protected@edef\theparentequation{\theequation}%
  \setcounter{parentequation}{\value{equation}}%
  \setcounter{equation}{0}%
  \def\theequation{(\theparentequation\alph{equation})}%
  \ignorespaces
}{%
  \setcounter{equation}{\value{parentequation}}%
  \ignorespacesafterend
}
%%%%
}{
%%%%
\renewenvironment{subequations}{%
\renewcommand{\theequation}{%
\ifnum\c@chapter>\z@\thechapter.\fi \@arabic\c@equation}
  \refstepcounter{equation}%
  \protected@edef\theparentequation{\theequation}%
  \setcounter{parentequation}{\value{equation}}%
  \setcounter{equation}{0}%
  \def\theequation{(\theparentequation\alph{equation})}%
  \ignorespaces
}{%
  \setcounter{equation}{\value{parentequation}}%
  \ignorespacesafterend
}
%%%%
}
}
%% (  )は \theequationにとりあえず入れたが、後で、検証

%% equationはここにあった


%%% COFFFブレーク
\newcounter{COFFequation}%[chapter]
%\@addtoreset{equation}{chapter}
\renewcommand{\theCOFFequation}{(\@arabic\c@COFFequation)}

\newenvironment{COFFequation}%
    {\@beginparpenalty\predisplaypenalty
     \@endparpenalty\postdisplaypenalty
     \refstepcounter{COFFequation}%
     \parsep  4\p@ \@plus2\p@ \@minus\p@
     \topsep  8\p@ \@plus2\p@ \@minus4\p@
     \itemsep 4\p@ \@plus2\p@ \@minus\p@
     \trivlist \item[]\leavevmode
       \hb@xt@\linewidth\bgroup $\m@th% $
         \displaystyle
         \hskip\mathindent}%
        {$\hfil % $
         \displaywidth\linewidth\hbox{\@COFFeqnnum}%
       \egroup
     \endtrivlist}


\renewenvironment{eqnarray}{%
    \stepcounter{equation}%
%    \parsep  4\p@ \@plus2\p@ \@minus\p@
    \topsep  8\p@ \@plus2\p@ \@minus4\p@
%    \itemsep 4\p@ \@plus2\p@ \@minus\p@
    \def\@currentlabel{\p@equation\theequation}%
    \global\@eqnswtrue\m@th
    \global\@eqcnt\z@
    \tabskip\mathindent
    \let\\=\@eqncr
    \setlength\abovedisplayskip{\topsep}%
    \ifvmode
      \addtolength\abovedisplayskip{\partopsep}%
    \fi
    \addtolength\abovedisplayskip{\parskip}%
    \setlength\belowdisplayskip{\abovedisplayskip}%
    \setlength\belowdisplayshortskip{\abovedisplayskip}%
    \setlength\abovedisplayshortskip{\abovedisplayskip}%
    $$\everycr{}\halign to\linewidth% $$
    \bgroup
      \hskip\@centering
%      $\displaystyle\tabskip\z@skip{##}$\@eqnsel&%
      $\displaystyle\tabskip\z@skip{##}$\hfill&%
%      \global\@eqcnt\@ne \hskip.8\arraycolsep ${##}$\hfil&%
%      \global\@eqcnt\tw@ \hskip.8\arraycolsep
       \global\@eqcnt\@ne \hfil${##}$\hfil&%
       \global\@eqcnt\tw@ 
        $\displaystyle{##}$\hfil \tabskip\@centering&%
      \global\@eqcnt\thr@@
        \hb@xt@\z@\bgroup\hss##\egroup\tabskip\z@skip\cr}%
      {\@@eqncr
    \egroup
    \global\advance\c@equation\m@ne$$% $$
    \@ignoretrue
    }


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{COFFeqnarray}{%
    \stepcounter{COFFequation}%
%    \parsep  4\p@ \@plus2\p@ \@minus\p@
    \topsep  8\p@ \@plus2\p@ \@minus4\p@
%    \itemsep 4\p@ \@plus2\p@ \@minus\p@
    \def\@currentlabel{\p@equation\theCOFFequation}%
    \global\@eqnswtrue\m@th
    \global\@eqcnt\z@
    \tabskip\mathindent
    \let\\=\@eqncr
    \setlength\abovedisplayskip{\topsep}%
    \ifvmode
      \addtolength\abovedisplayskip{\partopsep}%
    \fi
    \addtolength\abovedisplayskip{\parskip}%
    \setlength\belowdisplayskip{\abovedisplayskip}%
    \setlength\belowdisplayshortskip{\abovedisplayskip}%
    \setlength\abovedisplayshortskip{\abovedisplayskip}%
    $$\everycr{}\halign to\linewidth% $$
    \bgroup
%%%%%%%%%%%%%%%%%%%%% - from latex.ltx %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\@@eqncr{\let\reserved@a\relax
    \ifcase\@eqcnt \def\reserved@a{& & &}\or \def\reserved@a{& &}%
     \or \def\reserved@a{&}\else
       \let\reserved@a\@empty
       \@latex@error{Too many columns in eqnarray environment}\@ehc\fi
     \reserved@a \if@eqnsw\@COFFeqnnum\stepcounter{COFFequation}\fi
     \global\@eqnswtrue\global\@eqcnt\z@\cr}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      \hskip\@centering
%      $\displaystyle\tabskip\z@skip{##}$\@eqnsel&%
     $\displaystyle\tabskip\z@skip{##}$\hfill&%
%      \global\@eqcnt\@ne \hskip.8\arraycolsep ${##}$\hfil&%
%      \global\@eqcnt\tw@ \hskip.8\arraycolsep
       \global\@eqcnt\@ne ${##}$\hfil&%
       \global\@eqcnt\tw@ 
        $\displaystyle{##}$\hfil \tabskip\@centering&%
      \global\@eqcnt\thr@@
        \hb@xt@\z@\bgroup\hss##\egroup\tabskip\z@skip\cr}%
      {\@@eqncr
    \egroup
    \global\advance\c@COFFequation\m@ne$$% $$
%   \global\advance\c@equation\m@ne$$% $$
    \@ignoretrue
    }






%\@definecounter{COFFequation}
%\def\COFFequation{$$\refstepcounter{COFFequation}}
%\def\endCOFFequation{\eqno \hbox{\@COFFeqnnum}$$\@ignoretrue}
%\def\@COFFeqnnum{{\normalfont \normalcolor (\theCOFFequation)}}


\newcount\@COFFeqcnt
\newcount\@COFFeqpen
\newif\if@COFFeqnsw\@COFFeqnswtrue
\let\@COFFeqnsel=\relax
\def\COFFnonumber{\global\@COFFeqnswfalse}
\def\@COFFeqncr{%
   {\ifnum0=`}\fi
   \@ifstar{%
      \global\@COFFeqpen\@M\@COFFyeqncr
   }{%
      \global\@COFFeqpen\interdisplaylinepenalty \@COFFyeqncr
   }%
}
\def\@COFFyeqncr{\@testopt\@COFFxeqncr\z@skip}
\def\@COFFxeqncr[#1]{%
   \ifnum0=`{\fi}%
   \@@COFFeqncr
   \noalign{\penalty\@COFFeqpen\vskip\jot\vskip #1\relax}%
}

\def\@@COFFeqncr{\let\reserved@a\relax
    \ifcase\@COFFeqcnt \def\reserved@a{& & &}\or \def\reserved@a{& &}%
     \or \def\reserved@a{&}\else
       \let\reserved@a\@empty
       \@latex@error{Too many columns in eqnarray environment}\@ehc\fi
     \reserved@a \if@COFFeqnsw\@COFFeqnnum\stepcounter{COFFequation}\fi
     \global\@COFFeqnswtrue\global\@COFFeqcnt\z@\cr}

\let\@COFFseqncr=\@COFFeqncr


%\@namedef{COFFeqnarray*}{\def\@COFFeqncr{\COFFnonumber\@COFFseqncr}\COFFeqnarray}
%\@namedef{endCOFFeqnarray*}{\COFFnonumber\endCOFFeqnarray}

%\@namedef{COFFeqnarray*}{eqnarray*}
%\@namedef{endCOFFeqnarray*}{endeqnarray*}

\renewenvironment{COFFeqnarray}{%
    \stepcounter{COFFequation}%
%    \parsep  4\p@ \@plus2\p@ \@minus\p@
    \topsep  8\p@ \@plus2\p@ \@minus4\p@
%    \itemsep 4\p@ \@plus2\p@ \@minus\p@
    \def\@currentlabel{\p@COFFequation\theCOFFequation}%
    \global\@COFFeqnswtrue\m@th
    \global\@COFFeqcnt\z@
    \tabskip\mathindent
    \let\\=\@COFFeqncr
    \setlength\abovedisplayskip{\topsep}%
    \ifvmode
      \addtolength\abovedisplayskip{\partopsep}%
    \fi
    \addtolength\abovedisplayskip{\parskip}%
    \setlength\belowdisplayskip{\abovedisplayskip}%
    \setlength\belowdisplayshortskip{\abovedisplayskip}%
    \setlength\abovedisplayshortskip{\abovedisplayskip}%
    $$\everycr{}\halign to\linewidth% $$
    \bgroup
      \hskip\@centering
%      $\displaystyle\tabskip\z@skip{##}$\@eqnsel&%
      $\displaystyle\tabskip\z@skip{##}$\hfill&%
%      \global\@eqcnt\@ne \hskip.8\arraycolsep ${##}$\hfil&%
%      \global\@eqcnt\tw@ \hskip.8\arraycolsep
       \global\@COFFeqcnt\@ne \hfil${##}$\hfil&%
       \global\@COFFeqcnt\tw@ 
        $\displaystyle{##}$\hfil \tabskip\@centering&%
      \global\@COFFeqcnt\thr@@
        \hb@xt@\z@\bgroup\hss##\egroup\tabskip\z@skip\cr}%
      {\@@COFFeqncr
    \egroup
    \global\advance\c@COFFequation\m@ne$$% $$
    \@ignoretrue
    }







\renewcommand\[{\relax
                \ifmmode\@badmath
                \else
                 \parsep  4\p@ \@plus2\p@ \@minus\p@
                 \topsep  8\p@ \@plus2\p@ \@minus4\p@
                 \itemsep 4\p@ \@plus2\p@ \@minus\p@
                  \begin{trivlist}%
                    \@beginparpenalty\predisplaypenalty
                    \@endparpenalty\postdisplaypenalty
                    \item[]\leavevmode
                    \hb@xt@\linewidth\bgroup $\m@th\displaystyle %$
                      \hskip\mathindent\bgroup
                \fi}
\renewcommand\]{\relax
                \ifmmode
                      \egroup $\hfil% $
                    \egroup
                  \end{trivlist}%
                \else \@badmath
                \fi}











\if@enablejfam
  \DeclareSymbolFont{mincho}{JY1}{mc}{m}{n}
  \DeclareSymbolFontAlphabet{\mathmc}{mincho}
  \SetSymbolFont{mincho}{bold}{JY1}{gt}{m}{n}
  \DeclareMathAlphabet{\mathgt}{JY1}{gt}{m}{n}
  \reDeclareMathAlphabet{\mathrm}{\@mathrm}{\@mathmc}
  \reDeclareMathAlphabet{\mathbf}{\@mathbf}{\@mathgt}
  \jfam\symmincho
\else
  \DeclareRobustCommand{\mathmc}{%
    \@latex@error{Command \noexpand\mathmc invalid with\space
       `disablejfam' class option.}\@eha
  }
  \DeclareRobustCommand{\mathgt}{%
    \@latex@error{Command \noexpand\mathgt invalid with\space
       `disablejfam' class option.}\@eha
  }
\fi
\DeclareOldFontCommand{\mc}{\normalfont\mcfamily}{\mathmc}
\DeclareOldFontCommand{\gt}{\normalfont\gtfamily}{\mathgt}
\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareRobustCommand*{\cal}{\@fontswitch\relax\mathcal}
\DeclareRobustCommand*{\mit}{\@fontswitch\relax\mathnormal}
\setcounter{tocdepth}{2}
\newcommand{\@pnumwidth}{1.55em}
\newcommand{\@tocrmarg}{2.55em}
\newcommand{\@dotsep}{1}%{4.5}
\newdimen\toclineskip
\setlength\toclineskip{\z@}

\newdimen\@lnumwidth
%%\def\numberline#1{\hbox to\@lnumwidth{#1\hfil}}
%\def\numberline#1{\hbox to\@lnumwidth{#1}\hskip1zw}
\def\numberline#1{{#1}\hskip1zw}


\def\@dottedtocline#1#2#3#4#5{%
  \ifnum #1>\c@tocdepth \else
    \vskip\toclineskip \@plus.2\p@
    {\leftskip #2\relax \rightskip \@tocrmarg \parfillskip -\rightskip
     \parindent #2\relax\@afterindenttrue
     \interlinepenalty\@M
     \leavevmode
     \@lnumwidth #3\relax
     \advance\leftskip \@lnumwidth \hbox{}\hskip -\leftskip
     {#4}\nobreak
     \leaders\hbox{$\m@th \mkern \@dotsep mu.\mkern \@dotsep mu$}%
     \hfill\nobreak
     \hb@xt@\@pnumwidth{\hss\normalfont \normalcolor #5}%
     \par}%
  \fi}
\def\addcontentsline#1#2#3{%
  \protected@write\@auxout
    {\let\label\@gobble \let\index\@gobble \let\glossary\@gobble
\@temptokena{\thepage}}%
    {\string\@writefile{#1}%
       {\protect\contentsline{#2}{#3}{\the\@temptokena}}}%
}
\newcommand{\tableofcontents}{%
  \if@twocolumn\@restonecoltrue\onecolumn
  \else\@restonecolfalse\fi
%\pagenumbering{roman}%
%\@BUNRUI=\z@%
\renewcommand{\thepage}{\@roman\c@page}
%\pagestyle{Rheadings}%
  \chapter*{\contentsname}\vspace*{-.75\Cvs}%%%% koko
\thispagestyle{CHAPheadings}
    \@mkboth{\contentsname}{\contentsname}%
\@starttoc{toc}%
  \if@restonecol\twocolumn\fi
}


\newcommand*{\l@part}[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty{-\@highpenalty}%
    \addvspace{2.25em \@plus\p@}%
    \begingroup
    \parindent\z@\rightskip\@pnumwidth
    \parfillskip-\@pnumwidth
    {\leavevmode\large\bfseries
     \setlength\@lnumwidth{4zw}%
     #1\hfil\nobreak
     \hbox to\@pnumwidth{\hss#2}}\par
    \nobreak
    \global\@nobreaktrue
    \everypar{\global\@nobreakfalse\everypar{}}%
     \endgroup
  \fi}




\newcommand*{\l@chapter}[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \addvspace{1.0em \@plus\p@}%
    \begingroup
      \parindent\z@ \rightskip\@pnumwidth \parfillskip-\rightskip
      \leavevmode\bfseries
      \setlength\@lnumwidth{1zw}%{4zw}%
      \advance\leftskip\@lnumwidth \hskip-\leftskip
      #1\nobreak\hfil\nobreak\hbox to\@pnumwidth{\hss#2}\par
      \penalty\@highpenalty
    \endgroup
  \fi}



%%% 目次章階層 3Lドリ天地左右中央
\newdimen\TOCCHAPdimen
\TOCCHAPdimen=2\baselineskip 
\addtolength{\TOCCHAPdimen}{\topskip}%
\addtolength{\TOCCHAPdimen}{12H}%




\renewcommand*{\l@chapter}[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
%    \addvspace{1.5em \@plus\p@}%
%%%%%%%%%%%%%%%%%%%%
    \begingroup\vbox to\TOCCHAPdimen{\vskip13.5H\vfil
\centerline{
      \parindent\z@ \rightskip\@pnumwidth \parfillskip-\rightskip
      \leavevmode\large\bfseries
      \setlength\@lnumwidth{0zw}%{3zw}%
      \advance\leftskip\@lnumwidth \hskip-\leftskip
%      \centerline{\HASIRAkintou{#1}}%\nobreak\hfil%\nobreak\hbox to\@pnumwidth{\hss#2}
%      \centerline{
{\bfseries%\FutogoXvi%\HelveXvi
{#1}}}\vfil}%\nobreak\hfil%\nobreak\hbox to\@pnumwidth{\hss#2}
\par
      \penalty\@highpenalty
    \endgroup%\addvspace{1.5em \@plus\p@}%
  \fi}

\def\@BIBINDEXdottedtocline#1#2#3#4#5{%
  \ifnum #1>\c@tocdepth \else
    \vskip\toclineskip \@plus.2\p@
    {\leftskip #2\relax \rightskip \@tocrmarg \parfillskip -\rightskip
     \parindent #2\relax\@afterindenttrue
     \interlinepenalty\@M
%     \leavevmode\fontsize{14\JQ}{20H}\selectfont\bfseries
     \leavevmode\fontsize{14\JQ}{24H}\selectfont\bfseries
     \@lnumwidth #3\relax
     \advance\leftskip \@lnumwidth \hbox{}\hskip -\leftskip
     {#4}\nobreak
%     \leaders\hbox{$\m@th \mkern \@dotsep mu.\mkern \@dotsep mu$}%
\hskip2zw%     \hfill\nobreak
     \hb@xt@\@pnumwidth{\hss\normalfont \normalcolor
  \slshape\bfseries#5
}%
     \par}%
  \fi}



\def\@dottedtocline#1#2#3#4#5{%
  \ifnum #1>\c@tocdepth \else
    \vskip\toclineskip \@plus.2\p@
    {\leftskip #2\relax \rightskip \@tocrmarg \parfillskip -\rightskip
     \parindent #2\relax\@afterindenttrue
     \interlinepenalty\@M
     \leavevmode
     \@lnumwidth #3\relax
     \advance\leftskip \@lnumwidth \hbox{}\hskip -\leftskip
%     {\bfseries #4}\nobreak
     \SEVENjidori{#4}\nobreak
     \leaders\hbox{\raise .9mm\hbox{$\m@th \mkern \@dotsep mu.\mkern \@dotsep mu$}}%
     \hfill\nobreak
     \hb@xt@\@pnumwidth{\hss\normalfont \normalcolor \slshape#5}%
     \par}%
  \fi}





\newcommand*{\l@TUKIMONOchapter}[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
%    \addvspace{1.5em \@plus\p@}%
    \begingroup{%
      \parindent\z@ \rightskip\@pnumwidth \parfillskip-\rightskip
      \leavevmode\large\bfseries
      \setlength\@lnumwidth{0zw}%{3zw}%
      \advance\leftskip\@lnumwidth \hskip-\leftskip
%      \centerline{\HASIRAkintou{#1}}%\nobreak\hfil%\nobreak\hbox to\@pnumwidth{\hss#2}
%      \centerline{
{\bfseries%\FutogoXvi%\HelveXvi
\mokuSEVENjidori{#1}}}%\nobreak\hfil%\nobreak\hbox to\@pnumwidth{\hss#2}
\leaders\hbox{\raise .9mm\hbox{$\m@th \mkern \@dotsep mu.\mkern \@dotsep mu$}}%
     \hfill\nobreak
     \hb@xt@\@pnumwidth{\hss\normalfont \normalcolor \slshape #2}
\par
      \penalty\@highpenalty
    \endgroup%\addvspace{1.5em \@plus\p@}%
  \fi}


\def\@MMMMMTUKIMONOdottedtocline#1#2#3#4#5{%
  \ifnum #1>\c@tocdepth \else
    \vskip\toclineskip \@plus.2\p@
    {\leftskip #2\relax \rightskip \@tocrmarg \parfillskip -\rightskip
     \parindent #2\relax\@afterindenttrue
     \interlinepenalty\@M
     \leavevmode
     \@lnumwidth #3\relax
     \advance\leftskip \@lnumwidth \hbox{}\hskip -\leftskip
%     {\bfseries #4}\nobreak
     \SEVENjidori{#4}\nobreak
     \leaders\hbox{\raise .9mm\hbox{$\m@th \mkern \@dotsep mu.\mkern \@dotsep mu$}}%
     \hfill\nobreak
     \hb@xt@\@pnumwidth{\hss\normalfont \normalcolor \slshape\bfseries#5}%
     \par}%
  \fi}


\newcommand*{\l@section}{\@dottedtocline{1}{0em}{2.3em}}
\newcommand*{\l@subsection}   {\@dottedtocline{2}{1.5zw}{3.2em}}
\newcommand*{\l@subsubsection}{\@dottedtocline{3}{7.0em}{4.1em}}
\newcommand*{\l@paragraph}    {\@dottedtocline{4}{10em}{5em}}
\newcommand*{\l@subparagraph} {\@dottedtocline{5}{12em}{6em}}



\newcommand{\listoffigures}{%
  \if@twocolumn\@restonecoltrue\onecolumn
  \else\@restonecolfalse\fi
  \chapter*{\listfigurename
  \@mkboth{\listfigurename}{\listfigurename}}%
  \@starttoc{lof}%
  \if@restonecol\twocolumn\fi
}
\newcommand*{\l@figure}{\@dottedtocline{1}{1.5em}{2.3em}}
\newcommand{\listoftables}{%
  \if@twocolumn\@restonecoltrue\onecolumn
  \else\@restonecolfalse\fi
  \chapter*{\listtablename
  \@mkboth{\listtablename}{\listtablename}}%
  \@starttoc{lot}%
  \if@restonecol\twocolumn\fi
}
\let\l@table\l@figure








%%## citesort.sty ##%%
%% from "citesort.sty", a little customized
\newcount\@minsofar
\newcount\@min
\newcount\@cite@temp
\def\@citex[#1]#2{%\nolinebreak%
\if@filesw \immediate \write \@auxout {\string \citation {#2}}\fi
\@tempcntb\m@ne \let\@h@ld\relax \def\@citea{}%
\@min\m@ne%
\@cite{\hskip-\xkanjiskip%%
  \@for \@citeb:=#2\do {\@ifundefined {b@\@citeb}%
    {\@h@ld\@citea\@tempcntb\m@ne{\bfseries ?}%
    \@warning {Citation `\@citeb ' on page \thepage \space undefined}}%
{\@minsofar\z@ \@for \@scan@cites:=#2\do {%
  \@ifundefined{b@\@scan@cites}%
    {\@cite@temp\m@ne}
    {\@cite@temp\number\csname b@\@scan@cites \endcsname \relax}%
\ifnum\@cite@temp > \@min% select the next one to list
    \ifnum\@minsofar = \z@
      \@minsofar\number\@cite@temp
      \edef\@scan@copy{\@scan@cites}\else
    \ifnum\@cite@temp < \@minsofar
      \@minsofar\number\@cite@temp
      \edef\@scan@copy{\@scan@cites}\fi\fi\fi}\@tempcnta\@min
  \ifnum\@minsofar > \z@ % some more
    \advance\@tempcnta\@ne
    \@min\@minsofar
    \ifnum\@tempcnta=\@minsofar %   Number follows previous--hold on to it
      \ifx\@h@ld\relax
        \edef \@h@ld{\@citea\csname b@\@scan@copy\endcsname}%
      \else \edef\@h@ld{\ifmmode{)$\sim$}\else)$\sim$\fi
       \csname b@\@scan@copy\endcsname}%
      \fi
    \else \@h@ld\@citea\csname b@\@scan@copy\endcsname
          \let\@h@ld\relax
  \fi % no more
\fi}%
\def\@citea{),\penalty\@highpenalty\,}}\@h@ld}{#1}}
%% end of citesort.sty

\def\@cite#1#2{\leavevmode\unskip%
  \ifnum\lastpenalty=\z@\penalty\@highpenalty\fi% highpenalty before
$^{\mbox{%\footnotesize
\scriptsize\rm\mc{\multiply\@highpenalty 3 #1%             % triple-highpenalties within
      \if@tempswa,\penalty\@highpenalty\ #2\fi % and before note.
    })}}$\spacefactor\@m}





\def\@citeNx[#1]#2{%\nolinebreak%
\if@filesw \immediate \write \@auxout {\string \citation {#2}}\fi
\@tempcntb\m@ne \let\@h@ld\relax \def\@citea{}%
\@min\m@ne%
\@citeN{\hskip-\xkanjiskip%
  \@for \@citeb:=#2\do {\@ifundefined {b@\@citeb}%
    {\@h@ld\@citea\@tempcntb\m@ne{\bfseries ?}%
    \@warning {Citation `\@citeb ' on page \thepage \space undefined}}%
{\@minsofar\z@ \@for \@scan@cites:=#2\do {%
  \@ifundefined{b@\@scan@cites}%
    {\@cite@temp\m@ne}
    {\@cite@temp\number\csname b@\@scan@cites \endcsname \relax}%
\ifnum\@cite@temp > \@min% select the next one to list
    \ifnum\@minsofar = \z@
      \@minsofar\number\@cite@temp
      \edef\@scan@copy{\@scan@cites}\else
    \ifnum\@cite@temp < \@minsofar
      \@minsofar\number\@cite@temp
      \edef\@scan@copy{\@scan@cites}\fi\fi\fi}\@tempcnta\@min
  \ifnum\@minsofar > \z@ % some more
    \advance\@tempcnta\@ne
    \@min\@minsofar
    \ifnum\@tempcnta=\@minsofar %   Number follows previous--hold on to it
      \ifx\@h@ld\relax
        \edef \@h@ld{\@citea\csname b@\@scan@copy\endcsname}%
      \else \edef\@h@ld{\ifmmode{)$\sim$}\else)$\sim$\fi
       \csname b@\@scan@copy\endcsname}%
      \fi
    \else \@h@ld\@citea\csname b@\@scan@copy\endcsname
          \let\@h@ld\relax
  \fi % no more
\fi}%
\def\@citea{),\penalty\@highpenalty\,}}\@h@ld}{#1}}



\def\@citeN#1#2{\leavevmode\unskip%
  \ifnum\lastpenalty=\z@\penalty\@highpenalty\fi% highpenalty before
${\mbox{%\footnotesize
\rm\mc{\multiply\@highpenalty 3 #1%             % triple-highpenalties within
      \if@tempswa,\penalty\@highpenalty\ #2\fi % and before note.
    })}}$\spacefactor\@m}


\DeclareRobustCommand\citen{%
  \@ifnextchar [{\@tempswatrue\@citeNx}{\@tempswafalse\@citeNx[]}}
%\let\citen=\cite









\newdimen\bibindent
\setlength\bibindent{1.5em}
\newcommand{\newblock}{\hskip .11em\@plus.33em\@minus.07em}
%
\newenvironment{bibcomment}{%\setlength\labelsep{0zw}%
%\listparindent{-5zw}%
%\setlength{\leftmargin}{-10zw}
%\setlength\itemindent{-\labelwidth \advance\itemindent by-\labelsep}
\begin{indentation}{-\leftmargin}{0zw}
%\item[]{}
%
}{\end{indentation}}

%%%%%% 
\def\@biblabel#1{\hfill#1\hfill)}%
%\def\@biblabel#1{\hfill#1\hfill}%
%%% \sectionパターンとして、各章末に文献を入れるときは=  thesectbibliography アステを付ける
\newenvironment{thebibliography*}[1]
{\section*{引用・参考文献
%\@mkboth{\bibname}{\bibname}
}%
\addcontentsline{toc}{section}{引用・参考文献}%
\small
   \list{\@biblabel{\@arabic\c@enumiv}}%
        {\small\settowidth\labelwidth{\@biblabel{#1}}%
        \setlength\labelsep{1zw}%
         \leftmargin\labelwidth
         \advance\leftmargin\labelsep
         \@openbib@code
         \usecounter{enumiv}%
\markright{引用\hfill ・\hfill 参考文献}%
         \let\p@enumiv\@empty
         \renewcommand\theenumiv{\@arabic\c@enumiv}%
\topsep\z@\parsep\z@\partopsep\z@\itemsep\z@%
}%
   \sloppy
   \clubpenalty4000
   \@clubpenalty\clubpenalty
   \widowpenalty4000%
   \sfcode`\.\@m}
  {\def\@noitemerr
    {\@latex@warning{Empty `thebibliography' environment}}%
   \endlist}



%%% \chapter パターン = デフォルトとする。
\newenvironment{thebibliography}[1]
{%
%\def\@schapter##1{%
%\refstepcounter{chapter}%
%  \@makeAPPschapterhead{##1}\@afterheading
%}
%  \if@openright\clearpage\else\clearpage\fi
%\@makeAPPschapterhead{付録}%
\chapter*{引用・参考文献}%
\addtocontents{toc}{\protect\addvspace{3\h}}%
\addcontentsline{toc}{TUKIMONOchapter}{引用・参考文献}%
\addtocontents{toc}{\protect\addvspace{3\h}}%
\thispagestyle{CHAPheadings}
\@mkboth{引用\hfill ・\hfill 参考文献}{引用\hfill ・\hfill 参考文献}
%%%%%
%\chapter*{\bibname\@mkboth{\bibname}{\bibname}}%
\addvspace{6\h}%%%!!!
\bgroup\small
   \list{\@biblabel{\@arabic\c@enumiv}}%
        {\settowidth\labelwidth{\@biblabel{#1}}%
         \leftmargin\labelwidth
         \advance\leftmargin\labelsep
         \@openbib@code
         \usecounter{enumiv}%
         \let\p@enumiv\@empty
         \renewcommand\theenumiv{\@arabic\c@enumiv}%
%%
\topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
}%
   \sloppy
   \clubpenalty4000
   \@clubpenalty\clubpenalty
   \widowpenalty4000%
   \sfcode`\.\@m}
  {\def\@noitemerr
    {\@latex@warning{Empty `thebibliography' environment}}%
   \endlist\egroup}


\let\@openbib@code\@empty




\def\doubledash{\hbox to 2zw{---\hss ---}}

\newenvironment{theindex}
  {%\if@twocolumn\@restonecolfalse\else\@restonecoltrue\fi
	\columnseprule 0.12mm%\z@
	\columnsep=1zw
	\clearpage
\addcontentsline{toc}{TUKIMONOchapter}{索引}%
%\addtocontents{toc}{\protect\addvspace{1.25mm}}% 10Hアキ
%\addcontentsline{toc}{section}{%\rm\llarge 
%索　　　　引}%
%\multicolsep=.5\Cvs
	\begin{multicols}{3}[\chapter*{索引}][0pt]
%   \twocolumn[\@makeschapterhead{\indexname}]%
   \@mkboth{\indexname}{\indexname}%
\bgroup\footnotesize\baselineskip=16H%
   \thispagestyle{CHAPheadings}\parindent\z@
   \parskip\z@\relax
   \let\item\@idxitem}
  {\egroup\end{multicols}%\if@restonecol\onecolumn\else\clearpage\fi
\vspace*{-.25\Cvs}}




\newcommand{\@idxitem}{\par\hangindent 1zw}
\newcommand{\subitem}{\par\hangindent 1zw \hspace*{20pt}}
\newcommand{\subsubitem}{\par\hangindent 1zw \hspace*{30pt}}
\newcommand{\indexspace}[1]{%\par
\leavevmode
%
\nopagebreak\smash{\raisebox{-2.5mm}{\centerline{\fontsize{14\JQ}{17H}\selectfont【\textbf{#1}】}}}\par
\nopagebreak　\par\nopagebreak}




\newbox\KARAsakuinbox

\newenvironment{theEindex}{\def\indexspace##1{\par
\setbox\KARAsakuinbox=\hbox{##1}}%
	\footnotesize\baselineskip=16H%9pt%12pt
	\columnseprule 0.12mm%\z@
	\columnsep=1zw
%	\clearpage
\multicolsep=.5\Cvs
	\begin{multicols}{3}[
%\@makeINDEXschapterhead{索引}
%\chapter*{索○●引}
\noindent\INDhrulefill{\normalsize$\Diamond$}\INDhrulefill{\normalsize$\Diamond$}\INDhrulefill]%[10pt]
%	\columnsep 35pt\twocolumn[\@makeschapterhead{索 引}]
%	\@mkboth{索　　　　　　　　　引}{索　　　　　　　　　引}%
%	\pagestyle{INDheadings}%\thispagestyle{INDCHAPheadings}
\parindent\z@
	\parskip\z@ \relax\let\item\@idxitem}{%\pagestyle{INDheadings}
\end{multicols}%\pagestyle{INDheadings}
%\vspace*{-.25\Cvs}
}




\renewenvironment{theEindex}{\def\OFFindexspace##1{\par
\setbox\KARAsakuinbox=\hbox{##1}}%
	\footnotesize\baselineskip=16H%9pt%12pt
	\columnseprule 0.12mm%\z@
	\columnsep=1zw
%	\clearpage
\multicolsep=.5\Cvs
	\begin{multicols}{3}[
%\@makeINDEXschapterhead{索引}
%\chapter*{索○●引}
\noindent\INDhrulefill{\normalsize$\Diamond$}\INDhrulefill{\normalsize$\Diamond$}\INDhrulefill]%[10pt]
%	\columnsep 35pt\twocolumn[\@makeschapterhead{索 引}]
%	\@mkboth{索　　　　　　　　　引}{索　　　　　　　　　引}%
%	\pagestyle{INDheadings}%\thispagestyle{INDCHAPheadings}
\parindent\z@
	\parskip\z@ \relax\let\item\@idxitem}{%\pagestyle{INDheadings}
\end{multicols}%\pagestyle{INDheadings}
%\vspace*{-.25\Cvs}
}




\def\INDhrulefill{\leavevmode\leaders\hrule height 1mm depth -0.88mm\hfill\kern\z@}



\def\INDbulkei{\scalebox{.75}[1.25]{\hbox to 48mm{～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～\hss ～}}}



\renewcommand{\subitem}{\@idxitem \hspace*{1zw}}




%%%%%%%%%%%%% 脚注 footonote の設定


\def\@Mfnsymbol#1{\ifcase#1 \or % \ensuremath{
 \dagger\or
 {\dagger}{\dagger}\or
 {\dagger}{\dagger}{\dagger}\or
 {\dagger}{\dagger}{\dagger}{\dagger}\or
 {\dagger}{\dagger}{\dagger}{\dagger}{\dagger}\or
 {\dagger}{\dagger}{\dagger}{\dagger}{\dagger}{\dagger}\or
 {\dagger}{\dagger}{\dagger}{\dagger}{\dagger}{\dagger}{\dagger}\or
 {\dagger}{\dagger}{\dagger}{\dagger}{\dagger}{\dagger}{\dagger}{\dagger}\or
 {\dagger}{\dagger}{\dagger}{\dagger}{\dagger}{\dagger}%
  {\dagger}{\dagger}{\dagger}\or
 *\or {*}{*}\or {*}{*}{*}\or {*}{*}{*}{*}\or 
  {*}{*}{*}{*}{*}\or {*}{*}{*}{*}{*}{*}\or %% ((((((((((((((((((((
 a)\or b)\or c)\or d)\or e)\or f)\or g)\or h)\or i)\or j)\or
 k)\or l)\or m)\or n)\or o)\or p)\or q)\or r)\or s)\or t)\else
  \@ctrerr\fi}% }



%%%%%%% by Honda 
%%% 1ページに1個しか脚注がないとき、†のみ、2個以上なら、†1, †2 という設定
%%% \footnote{文章}  ただし\footnote[]{}設定はない
%%%
%%% 以下2つはデフォルトの仕様で、\footnote とは連動しない
%%% \footnotemark[1] 普通に使える
%%% \footnotetext[1] 普通に使える



%\def\@makefnmark{\hbox{\@textsuperscript{$\dagger$\normalfont\@thefnmark}}}
%%%番号が消えた場合に見えるように取りあえず
\let\org@footnote\footnote
\newcount\ftID

\def\@makefnmark{\hbox{\@textsuperscript{$\dagger$\normalfont\@thefnmark}}}
%%%番号が消えた場合に見えるように取りあえず


\def\prev@ft@page{\relax}

\def\ft@ID@page#1#2{%
   \def\curr@page{#2}%
   \ifx\prev@ft@page\curr@page\else
      \global\@namedef{reset@ftno@#1}{\relax}%
   \fi
   \ifx\curr@page\prev@ft@page
      \@tempcnta#1\relax
      \advance\@tempcnta\m@ne 
      \@ifundefined{vanish@ftno@\the\@tempcnta}%
         {\relax}%
         {\global\expandafter\let
          \csname vanish@ftno@\the\@tempcnta\endcsname
          \@undefined}%
   \else
      \global\@namedef{vanish@ftno@#1}{\relax}%
   \fi
   \def\prev@ft@page{#2}%
}

\def\footnote#1{%
\global\advance\ftID\@ne%%%add global 2005/08/26 honda
\global\let\saved@thefootnote\thefootnote%%%add global 2005/08/26 honda
\@ifundefined{reset@ftno@\the\ftID}%
   {\relax}%
   {\setcounter{footnote}{\z@}}%
\@ifundefined{vanish@ftno@\the\ftID}%
   {\relax}%
   {\let\thefootnote\@empty}%
\org@footnote{#1}%
\global\let\thefootnote\saved@thefootnote%%%add global 2005/08/26 honda
\protected@write\@auxout{}%
{\string\ft@ID@page{\the\ftID}{\thepage}}%
}





%%%%%%%%%%%%%%%%%%%%% ここまで が特殊な脚注の動作


%%%% ここからは、脚注レイアウト

%\renewcommand{\thefootnote}{\fnsymbol{footnote}}

%%%%%%%
    \def\@makefnmark{\hbox{\ifydir
\footnotesize%
%{\ifnum \c@footnote =1$\m@th^{\dagger}$\else$\m@th^{\dagger\@thefnmark}$\fi}%
{$\m@th^{\dagger\@thefnmark}$}%
      \else\hbox{\yoko$\m@th^{\@thefnmark}$}\fi}}%

\renewcommand{\footnoterule}{%
  \kern.125\Cvs% %% 本文と脚注のアキ
  \hrule height .12mm width 50mm
  \kern .875mm% 罫線と脚注文字の上は2.5mmあき
}

%\@addtoreset{footnote}{page}


\newcommand\@makefntext[1]{\footnotesize\baselineskip15\h\parindent 2.75mm
\setlength{\leftmargin}{33Q}\advance\linewidth
-\leftmargin
\advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
  \noindent\leavevmode\hspace*{-11Q}%
\hbox to11Q{\hss
%{\ifnum \c@footnote =1$\m@th^{\dagger}$\else$\m@th^{\dagger\@thefnmark}$\fi}\hskip11Q}%
{$\m@th^{\dagger\@thefnmark}$}\hskip11Q}%
%\raggedright
#1}

%%%%%%%%%%%%% 脚注 終わり %%%%%%%%%%%%%%%%%%%%%%%





%%%% ギリシャの立体、Pifonとバッティングしないようにした %%%%%%
%%%   by T. Honda
%%%% All Rights Reserved (c) by T. Honda

\newcommand{\tempPifont}[1]{\fontfamily{#1}\fontencoding{U}%
\fontseries{m}\fontshape{n}\selectfont}
\newcommand{\tempPisymbol}[2]{{\tempPifont{#1}\char#2}}

\def\alphaup{\mathalpha{\mbox{\tempPisymbol{psy}{'141}}}}
\def\betaup{\mathalpha{\mbox{\tempPisymbol{psy}{'142}}}}
\def\xiup{\mathalpha{\mbox{\tempPisymbol{psy}{'143}}}}
\def\deltaup{\mathalpha{\mbox{\tempPisymbol{psy}{'144}}}}
\def\varepsilonup{\mathalpha{\mbox{\tempPisymbol{psy}{'145}}}}
\def\phiup{\mathalpha{\mbox{\tempPisymbol{psy}{'146}}}}
\def\gammaup{\mathalpha{\mbox{\tempPisymbol{psy}{'147}}}}
\def\etaup{\mathalpha{\mbox{\tempPisymbol{psy}{'150}}}}
\def\iotaup{\mathalpha{\mbox{\tempPisymbol{psy}{'151}}}}
\def\varphiup{\mathalpha{\mbox{\tempPisymbol{psy}{'152}}}}
\def\kappaup{\mathalpha{\mbox{\tempPisymbol{psy}{'153}}}}
\def\lambdaup{\mathalpha{\mbox{\tempPisymbol{psy}{'154}}}}
\def\muup{\mathalpha{\mbox{\tempPisymbol{psy}{'155}}}}
\def\nuup{\mathalpha{\mbox{\tempPisymbol{psy}{'156}}}}
\def\omicronup{\mathalpha{\mbox{\tempPisymbol{psy}{'157}}}}
\def\piup{\mathalpha{\mbox{\tempPisymbol{psy}{'160}}}}
\def\thetaup{\mathalpha{\mbox{\tempPisymbol{psy}{'161}}}}
\def\rhoup{\mathalpha{\mbox{\tempPisymbol{psy}{'162}}}}
\def\sigmaup{\mathalpha{\mbox{\tempPisymbol{psy}{'163}}}}
\def\tauup{\mathalpha{\mbox{\tempPisymbol{psy}{'164}}}}
\def\upsilonup{\mathalpha{\mbox{\tempPisymbol{psy}{'165}}}}
\def\varpiup{\mathalpha{\mbox{\tempPisymbol{psy}{'166}}}}
\def\omegaup{\mathalpha{\mbox{\tempPisymbol{psy}{'167}}}}
%\def\xiup{\mathalpha{\mbox{\tempPisymbol{psy}{'170}}}}
\def\chiup{\mathalpha{\mbox{\tempPisymbol{psy}{'170}}}}
\def\psiup{\mathalpha{\mbox{\tempPisymbol{psy}{'171}}}}
\def\zetaup{\mathalpha{\mbox{\tempPisymbol{psy}{'172}}}}
\def\varthetaup{\mathalpha{\mbox{\tempPisymbol{psy}{'112}}}}
\def\varzetaup{\mathalpha{\mbox{\tempPisymbol{psy}{'126}}}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%







\newif\if西暦 \西暦false
\def\西暦{\西暦true}
\def\和暦{\西暦false}
\newcount\heisei \heisei\year \advance\heisei-1988\relax
\def\today{{%
  \iftdir
    \if西暦
      \kansuji\number\year 年
      \kansuji\number\month 月
      \kansuji\number\day 日
    \else
      平成\ifnum\heisei=1 元年\else\kansuji\number\heisei 年\fi
      \kansuji\number\month 月
      \kansuji\number\day 日
    \fi
  \else
    \if西暦
      \number\year~年
      \number\month~月
      \number\day~日
    \else
      平成\ifnum\heisei=1 元年\else\number\heisei~年\fi
      \number\month~月
      \number\day~日
    \fi
  \fi}}
\newcommand{\prepartname}{第}
\newcommand{\postpartname}{部}
\newcommand{\prechaptername}{第}
\newcommand{\postchaptername}{章}
\newcommand{\contentsname}{目 次}
\newcommand{\listfigurename}{図 目 次}
\newcommand{\listtablename}{表 目 次}
\newcommand{\bibname}{文献}
\newcommand{\indexname}{索引}
\newcommand{\figurename}{図}
\newcommand{\tablename}{表}
\newcommand{\appendixname}{付 録}
\pagestyle{headings}
\pagenumbering{arabic}
\raggedbottom
\if@twocolumn
  \twocolumn
  \sloppy
  \flushbottom
\else
  \onecolumn
\fi
\if@twoside
  \@mparswitchtrue
\else
  \@mparswitchfalse
\fi





%%%% 35行
\setlength{\textheight}{27\Cvs}%%%%% 28L
\addtolength{\textheight}{\topskip}% 

%%%% 版面
\setlength{\textwidth}{35\Cwd} %% 行幅
\setlength\paperheight {210mm}% 	a5を特定する
\setlength\paperwidth  {148mm}%
%\setlength{\footskip}{8mm}

%%% 段落
\setlength{\parindent}{1zw}
\setlength{\parskip}{0mm}




\iftombow
\setlength{\topmargin}{-13.5mm}%
\setlength{\oddsidemargin}{-8.375mm}%
\setlength{\evensidemargin}{\oddsidemargin}
\hoffset=-12mm
\else
\setlength{\topmargin}{-13.15mm}%
\setlength{\oddsidemargin}{-8mm}%
\setlength{\evensidemargin}{\oddsidemargin}
\fi





%%%%%%%%%%%%%%%% この辺に
%%%%%%%%%%%%%%%% 新定理系環境を入れる



%%%%%%%%
%% 解答 

\def\KAITOUmoto{\@ifnextchar[{\KAITOUhikisu}{\KAITOUno}%
}
\def\endKAITOUmoto{\nopagebreak}


\long\def\KAITOUhikisu[#1]{%%
\everypar{\noindent\hspace*{-\parindent}%
\<【{\bfseries 解答}】\<\hskip1zw{(#1)}%
\hskip1zw\nopagebreak
\everypar{}}}
\let\endKAITOUhikisu\endtrivlist



\def\DIAsuiteQED{{\unskip\nobreak\hfil\penalty50
 \hskip1zw\hbox{}\nobreak\hfil \hbox{$\diamondsuit$}
 \parfillskip\z@ \finalhyphendemerits\z@\par}}



\long\def\KAITOUno{%\par\noindent%
\everypar{\noindent\hspace*{-\parindent}%
\<【{\bfseries 解答}】\<%
\hskip1zw\nopagebreak
\everypar{}}}
\let\endKAITOUno\endtrivlist

\newenvironment{解答}{%
\par\noindent
\bgroup\vskip.5mm%-2.75mm%.5\topsep 25Hアキ
%\topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
%\topsep0pt
\small\baselineskip20\h
  \setlength{\leftmargin}{1zw}%
  \setlength{\rightmargin}{1zw}%
  \advance\linewidth -\leftmargin
  \advance\linewidth -\rightmargin
  \advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
\begin{KAITOUmoto}
}{\DIAsuiteQED\end{KAITOUmoto}%
\vskip1.875mm%-6.125mm%
\egroup\par}





\newcommand{\prefacename}{まえがき}
\newenvironment{preface}[2]{\gdef\@AUTHOR{{\small
  #1}\par\hfill{\fontsize{14\JQ}{19H}\selectfont#2{\normalsize 　}}}%
  \if@twocolumn\@restonecoltrue\onecolumn
  \else\@restonecolfalse\fi
%\pagestyle{PREFACEheadings}
%  \chapter*{\contentsname
%    \@mkboth{\contentsname}{\contentsname}%
%  }
%\pagenumbering{roman}%
%\pagestyle{Rheadings}%
\renewcommand{\thepage}{\@roman\c@page}
%\@BUNRUI=\z@
%\ROMANnumbertrue
\chapter*{\prefacename}%
\thispagestyle{CHAPheadings}%
\@mkboth{\prefacename}{\prefacename}%
%\addcontentsline{toc}{PREFACE}{は　し　が　き}
  \if@restonecol\twocolumn\fi
}{\par\@AUTHOR%\par
\clearpage}




\renewenvironment{preface}[2]{\gdef\@AUTHOR{{\small
  #1}%\par\hfill
{\begin{indentation}{0zw}{1zw}\begin{flushright}\fontsize{14\JQ}{19H}\selectfont#2\end{flushright}\end{indentation}%
%{\normalsize 　}
}}%
  \if@twocolumn\@restonecoltrue\onecolumn
  \else\@restonecolfalse\fi
%\pagestyle{PREFACEheadings}
%  \chapter*{\contentsname
%    \@mkboth{\contentsname}{\contentsname}%
%  }
%\pagenumbering{roman}%
%\pagestyle{Rheadings}%
\renewcommand{\thepage}{\@roman\c@page}
%\@BUNRUI=\z@
%\ROMANnumbertrue
\chapter*{\prefacename}%
\thispagestyle{CHAPheadings}%
\@mkboth{\prefacename}{\prefacename}%
%\addcontentsline{toc}{PREFACE}{は　し　が　き}
  \if@restonecol\twocolumn\fi
}{\par\@AUTHOR%\par
\clearpage}


%%% from corona.sty 
%%% version 2.80 Copyright (C) 1993-1998 by Mitsunori Makino
% 不等号
%
%%%\def\FRAC#1#2{\leavevmode\kern-.1em
%%%  \raise.5ex\hbox{\the\scriptfont0 #1}\kern-.1em
%%%  /\kern-.15em\lower.25ex\hbox{\the\scriptfont0 #2}}

%%% 2006/11/9 \caption \section などでエラーとなるため、
%%% マクロを書き換えということになり、コメントアウト
%\def\leq{\mathrel{\mathpalette\gl@align<}}% less than or equal
%\def\geq{\mathrel{\mathpalette\gl@align>}}% greater than or equal
\def\gl@align#1#2{\lower.6ex\vbox{\baselineskip\z@skip\lineskip\z@
\ialign{$\m@th#1\hfil##\hfil$\crcr#2\crcr=\crcr}}}


%% \leq, \geq を書き換え \captionでもエラーは回避
\DeclareRobustCommand{\leq}{\mathrel{\mathpalette\gl@align<}}
\DeclareRobustCommand{\geq}{\mathrel{\mathpalette\gl@align>}}


%
% 分数
%
\def\Frac#1#2{\displaystyle{\frac{\displaystyle #1}{\displaystyle #2}}}


\newcommand{\bi}{\bfseries\slshape}




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% end old corona.sty


%
%%%%%%%%% 表の中の脚注 マクロはここから
\newcounter{footnote@tab}

\def\footnote@tab{%
   \@ifstar{\@@footnote@tab[0]}{\@@footnote@tab}%
}



\def\@@footnote@tab{\@ifnextchar[%]
   {\@footnote@tab}
   {\refstepcounter{footnote@tab}%
    \@footnote@tab[\the\c@footnote@tab]}%
}%


\def\@footnote@tab[#1]#2{%
%   \@ifundefined{footnote@tab@#1}%
%      {%
%%%%%%%%%%%%%%%%%%%
      \ifnum#1=\z@
         \@makefnmark@tab{\relax}%
         \refstepcounter{footnote@tab}%
         \global\@namedef{footnote@tab@1}{#2}%
      \else
         \@makefnmark@tab{#1}%
         \global\@namedef{footnote@tab@#1}{#2}%
      \fi
%      }%
%%%%%%%%%%%%%%%%%%%
%      {\relax}%%%あとでエラーにする
}




\def\tablefootnotesep{1mm}

\def\@makefnmark@tab#1{\hbox{\@textsuperscript{$\ast$\normalfont#1}}}

%%%% \let\@footnotemark\@footnotemark@tab

\def\@makefntext@tab#1{\scriptsize%
         \ifnum\c@footnote@tab=\@ne
            \let\temp@\relax%
         \else
           \def\temp@{\the\count@}%
         \fi
         \global\advance\count@\@ne
         \setbox\z@=\hbox{\hskip.5zw
            \@makefnmark@tab{\temp@}%
            \hskip.5zw}%
         \hangindent\wd\z@\noindent\copy\z@#1}


\def\putfootnote#1#2{%
\multispan{#1}%
   \global\count@\z@
\bgroup
   \let\\\relax
   \let\multicolumn\relax
   \let\@nameuse\relax
   \let\footnote@list\@empty
   \let\@makefntext@tab\relax
   \loop\ifnum\count@<\c@footnote@tab
   \advance\count@\@ne
   \xdef\footnote@list{\footnote@list
      \multicolumn{#1}{@{}p{#2}@{}}{%
         \@makefntext@tab
         \@nameuse{footnote@tab@\the\count@}}%
      \\}%
   \repeat
\egroup
\\\noalign{\vskip\tablefootnotesep}
\footnote@list%
\multispan{#1}\reset@footnote@tab%
}%


\def\reset@footnote@tab{%
   \count@\z@
   \loop\ifnum\count@<\c@footnote@tab
      \advance\count@\@ne
      \global\expandafter\let\csname footnote@tab@\the\count@\endcsname\relax
      \setcounter{footnote@tab}{\z@}
   \repeat%
}


\let\tabfootnote\footnote@tab

%%%%%%%%%ここまで






\pagestyle{headings}

%%%% \everymath={\displaystyle} amsmath.sty を利用の指示がきたので、
%%%% AtBeginDocument の中に移動した


\ifx\@Hxfloat\@Hundef\else\expandafter\endinput\fi
\let\@Hxfloat\@xfloat
\def\@xfloat#1[{\@ifnextchar{H}{\@HHfloat{#1}[}{\@Hxfloat{#1}[}}
\def\@HHfloat#1[H]{%
\expandafter\let\csname end#1\endcsname\end@Hfloat
\vskip\intextsep\vbox\bgroup\let\center=\Center\def\@captype{#1}\parindent\z@
\ignorespaces}
\def\end@Hfloat{\egroup \vskip \intextsep}






\endinput

    
%%
%% End of file `corona-a5.cls'.



基本設定

\DeclareFontShape{JY1}{mc}{m}{n}{<6> jis
 <5> s * [1.1828] % 8級 tiny
 <7> s * [1.056072] jis      % 10級  scriptsize
 <8> s * [1.01647] jis      % 11級  footnotesize
 <9> s * [0.9856] jis      % 12級  small
 <10> s * [0.961] jis      % 13級  normalsize
 <10.95> s * [0.94089] jis % 14級  large
 <12> s * [0.985694] jis    % 16級  Large
 <14.4> s * [0.924088] jis  % 18級  LARGE
 <17.28> s * [0.85561] jis % 20級  huge
 <20.74> s * [0.85540] jis % 24級  Huge
 <24.88> s * [0.9508] jis  % 32級  HUGE
 <-> jis
 }{}



 \DeclareFontShape{JY1}{mc}{bx}{n}{<6> jisg
 <5> s * [1.1828] % 8級 tiny
 <7> s * [1.056072] jisg      % 10級  scriptsize
 <8> s * [1.01647] jisg      % 11級  footnotesize
 <9> s * [0.9856] jisg      % 12級  small
 <10> s * [0.961] jisg      % 13級  normalsize
 <10.95> s * [0.94089] jisg % 14級 large
 <12> s * [0.985694] jisg    % 16級  Large
 <14.4> s * [0.924088] jisg  % 18級  LARGE
 <17.28> s * [0.85561] jisg % 20級  huge
 <20.74> s * [0.85540] jisg % 24級  Huge
 <24.88> s * [0.9508] jisg  % 32級  HUGE
 <-> jisg%%%min10
 }{}




%%%%%%%%%%% 旧 定義
%%
\newcounter{TEIRIcount}[chapter]
\renewcommand{\theTEIRIcount}{\thechapter.\@arabic\c@TEIRIcount}

\def\TEIRImoto{\@ifnextchar[{\TEIRIhikisu}{\TEIRIno}%
}
\def\endTEIRImoto{\nopagebreak}


\long\def\TEIRIhikisu[#1]{\par\refstepcounter{TEIRIcount}%
%%%%
\setlength{\leftmargin}{1zw}%
  \setlength{\rightmargin}{1zw}%
  \advance\linewidth -\leftmargin
  \advance\linewidth -\rightmargin
  \advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
%%%%
\noindent\mbox{{\bfseries 定理\theTEIRIcount\hskip1zw{\mc\rm(#1)}}}\par}
\let\endTEIRIhikisu\endtrivlist

\long\def\TEIRIno{\par\refstepcounter{TEIRIcount}%
%%%%
\setlength{\leftmargin}{1zw}%
  \setlength{\rightmargin}{1zw}%
  \advance\linewidth -\leftmargin
  \advance\linewidth -\rightmargin
  \advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
%%%%
\noindent\mbox{{\bfseries 定理\theTEIRIcount}}\hskip1zw\par}
\let\endTEIRIno\endtrivlist

\newenvironment{定理}{%
\par\noindent\leavevmode\leaders\hrule height2pt\hfill\kern\z@\par\vskip-5.5mm
\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par
%\hrulefill height .4mm
\bgroup  \begin{TEIRImoto}
%\begin{TEIRImoto}
}{\par\nopagebreak\end{TEIRImoto}%
\egroup\par
\vskip-2.125mm%8.375mm
\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par
\vskip-5mm
\noindent\leavevmode\leaders\hrule height2pt\hfill\kern\z@\par
}




%% 定義
\newcounter{TEIGIcount}[chapter]
\renewcommand{\theTEIGIcount}{\thechapter.\@arabic\c@TEIGIcount}

\def\TEIGImoto{\@ifnextchar[{\TEIGIhikisu}{\TEIGIno}%
}
%%%\let\endTEIGImoto\endtrivlist

%%%%%% TEST endlist
\def\endTEIGImotoTEST{\nopagebreak%
  \if@inlabel
    \leavevmode
    \global \@inlabelfalse 
  \fi
  \if@newlist
    \@noitemerr 
    \global \@newlistfalse 
  \fi A
  \ifhmode \unskip \par \fi\nopagebreak
  \if@noparlist \else %B
    \ifdim\lastskip >\z@ 
      \@tempskipa\lastskip \vskip -\lastskip
      \advance\@tempskipa\parskip \advance\@tempskipa -\@outerparskip C
      \vskip\@tempskipa\nopagebreak 
    \fi 
    \@endparenv D
  \fi E\nopagebreak
}
%%%%%%%%%%%%%%%%%

\def\endTEIGImoto{\nopagebreak}%



\long\def\TEIGIhikisu[#1]{\par\refstepcounter{TEIGIcount}%
\noindent\mbox{{\bfseries 定義\theTEIGIcount\hskip1zw\nobreak{\mc\rm(#1)}}}\par}
\let\endTEIGIhikisu\endtrivlist

\long\def\TEIGIno{\par\refstepcounter{TEIGIcount}%
\noindent\mbox{{\bfseries 定義\theTEIGIcount}}\hskip1zw\par\nopagebreak}
\let\endTEIGIno\endtrivlist

\newenvironment{定義}{%
\par\noindent\leavevmode\leaders\hrule height2pt\hfill\kern\z@\par\vskip-5.5mm
\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par
%\hrulefill height .4mm
\bgroup  
\setlength{\leftmargin}{1zw}%
  \setlength{\rightmargin}{1zw}%
  \advance\linewidth -\leftmargin
  \advance\linewidth -\rightmargin
  \advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
\begin{TEIGImoto}
}{\par\end{TEIGImoto}%
\egroup
\vskip-2.125mm%8.375mm
\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par
\vskip-5mm
\noindent\leavevmode\leaders\hrule height2pt\hfill\kern\z@\par
}




%% 補題
\newcounter{HODAIcount}[chapter]
\renewcommand{\theHODAIcount}{\thechapter.\@arabic\c@HODAIcount}

\def\HODAImoto{\@ifnextchar[{\HODAIhikisu}{\HODAIno}%
}
\def\endHODAImoto{\nopagebreak}


\long\def\HODAIhikisu[#1]{\par\refstepcounter{HODAIcount}%
\noindent\mbox{{\bfseries 補題\theHODAIcount\hskip1zw\nobreak{\mc\rm(#1)}}}\par}
\let\endHODAIhikisu\endtrivlist

\long\def\HODAIno{\par\refstepcounter{HODAIcount}%
\noindent\mbox{{\bfseries 補題\theHODAIcount}}\hskip1zw\par\nopagebreak}
\let\endHODAIno\endtrivlist

\newenvironment{補題}{%
\par\noindent\leavevmode\leaders\hrule height2pt\hfill\kern\z@\par\vskip-5.5mm
\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par
%\hrulefill height .4mm
\bgroup  \setlength{\leftmargin}{1zw}%
  \setlength{\rightmargin}{1zw}%
  \advance\linewidth -\leftmargin
  \advance\linewidth -\rightmargin
  \advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
\begin{HODAImoto}
}{\par\nopagebreak\end{HODAImoto}%
\egroup\par
\vskip-2.125mm%8.375mm
\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par
\vskip-5mm
\noindent\leavevmode\leaders\hrule height2pt\hfill\kern\z@\par
}





%% 証明 proof

\def\SHOUMEImoto{\@ifnextchar[{\SHOUMEIhikisu}{\SHOUMEIno}%
}
\def\endSHOUMEImoto{\nopagebreak}


\long\def\SHOUMEIhikisu[#1]{%%
\everypar{%
\noindent\hspace*{-\parindent}\smash{\raisebox{-1.25mm}{\framebox(9,5){{\bfseries
証明}}}}\hskip1zw{(#1)}\hskip1zw\nopagebreak\everypar{}}}
\let\endSHOUMEIhikisu\endtrivlist


\long\def\SHOUMEIno{%\par\noindent%
\everypar{\noindent\hspace*{-\parindent}\smash{\raisebox{-1.25mm}{\framebox(9,5){{\bfseries 証明}}}\hskip1zw\nopagebreak}\everypar{}}}
\let\endSHOUMEIno\endtrivlist


\def\SPADEsuiteQED{{\unskip\nobreak\hfil\penalty50
 \hskip1zw\hbox{}\nobreak\hfil \hbox{$\spadesuit$}
 \parfillskip\z@ \finalhyphendemerits\z@\par}}

\newenvironment{証明}{%
\par\noindent
\bgroup\vskip.5mm%-2.75mm%.5\topsep 25Hアキ
\small\baselineskip20\h%\topsep\z@\parsep\z@\partopsep\z@\itemsep\z@
%\topsep0pt
  \setlength{\leftmargin}{1zw}%
  \setlength{\rightmargin}{1zw}%
  \advance\linewidth -\leftmargin
  \advance\linewidth -\rightmargin
  \advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
\begin{SHOUMEImoto}
}{\SPADEsuiteQED\end{SHOUMEImoto}%
\vskip1.875mm%-6.125mm
\egroup\par}








%% 例題
\newcounter{REIDAIcount}[chapter]
\renewcommand{\theREIDAIcount}{\thechapter.\@arabic\c@REIDAIcount}

\def\REIDAImoto{\@ifnextchar[{\REIDAIhikisu}{\REIDAIno}%
}
\def\endREIDAImoto{\nopagebreak}


\long\def\REIDAIhikisu[#1]{\par\refstepcounter{REIDAIcount}%
\noindent\hspace*{-\parindent}\mbox{{\bfseries 例題\theREIDAIcount\hskip1zw\nobreak{\mc\rm(#1)}}}\par}
\let\endREIDAIhikisu\endtrivlist

\long\def\REIDAIno{\par\refstepcounter{REIDAIcount}%
\everypar{\noindent\hspace*{-\parindent}\mbox{{\bfseries 例題\theREIDAIcount}}\hskip1zw\everypar{}}\nopagebreak}
\let\endREIDAIno\endtrivlist

\newenvironment{例題}{\vskip-5\h%%
\par\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par
%\hrulefill height .4mm
\bgroup  \setlength{\leftmargin}{1zw}%
  \setlength{\rightmargin}{1zw}%
  \advance\linewidth -\leftmargin
  \advance\linewidth -\rightmargin
  \advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
\begin{REIDAImoto}
}{\par\nopagebreak\end{REIDAImoto}%
\egroup\par
\vskip-2.125mm%8.375mm
\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 例 (例題に似ているけれど区別されている)
\newcounter{REIcount}[chapter]
\renewcommand{\theREIcount}{\thechapter.\@arabic\c@REIcount}

\def\REImoto{\@ifnextchar[{\REIhikisu}{\REIno}%
}
\def\endREImoto{\nopagebreak}


\long\def\REIhikisu[#1]{\par\refstepcounter{REIcount}%
\everypar{\noindent\hspace*{-\parindent}\mbox{{\bfseries 例\theREIcount\hskip1zw\nobreak{\mc\rm(#1)}}}\everypar{}\hskip1zw}}
\let\endREIhikisu\endtrivlist

\long\def\REIno{\par\refstepcounter{REIcount}%
\everypar{\noindent\hspace*{-\parindent}\mbox{{\bfseries 例\theREIcount}}\hskip1zw\everypar{}}\nopagebreak}
\let\endREIno\endtrivlist

\newenvironment{例}{\vskip-5\h%%
\par\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par\nopagebreak
%\hrulefill height .4mm
\bgroup  \setlength{\leftmargin}{1zw}%
  \setlength{\rightmargin}{1zw}%
  \advance\linewidth -\leftmargin
  \advance\linewidth -\rightmargin
  \advance\@totalleftmargin\leftmargin
  \@setpar{{\@@par}}%
  \parshape 1 \@totalleftmargin \linewidth
  \ignorespaces
\begin{REImoto}
}{\par\nopagebreak\end{REImoto}%
\egroup\par
\vskip-2.125mm%8.375mm
\noindent\leavevmode\leaders\hrule height.12mm\hfill\kern\z@\par
}




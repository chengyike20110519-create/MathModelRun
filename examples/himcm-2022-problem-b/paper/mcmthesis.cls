%%
%% This is file `mcmthesis.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% mcmthesis.dtx  (with options: `class')
%% 
%% -----------------------------------
%% This is a generated file.
%% 
%% Copyright (C) 2010 -- 2015 by latexstudio
%%       2014 -- 2019 by Liam Huang
%%       2019 -- present by latexstudio.net
%% 
%% This work may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either version 1.3
%% of this license or (at your option) any later version.
%% The latest version of this license is in
%%   http://www.latex-project.org/lppl.txt
%% and version 1.3 or later is part of all distributions of LaTeX
%% version 2005/12/01 or later.
%% 
%% The Current Maintainer of this work is latexstudio.net.
%% 
\NeedsTeXFormat{LaTeX2e}[1999/12/01]
\ProvidesClass{mcmthesis}
  [2024/01/22 v6.3.3 The Thesis Template Designed For MCM/ICM]
\typeout{The Thesis Template Designed For MCM/ICM}
\def\MCMversion{v6.3.3}
\RequirePackage{xkeyval}
\RequirePackage{etoolbox}
\define@boolkey{MCM}[MCM@opt@]{CTeX}[false]{}
\define@boolkey{MCM}[MCM@opt@]{titlepage}[true]{}
\define@boolkey{MCM}[MCM@opt@]{abstract}[true]{}
\define@boolkey{MCM}[MCM@opt@]{sheet}[true]{}
\define@boolkey{MCM}[MCM@opt@]{titleinsheet}[false]{}
\define@boolkey{MCM}[MCM@opt@]{keywordsinsheet}[false]{}
\define@cmdkeys{MCM}[MCM@opt@]{tcn,problem,tstyle}
\define@key{MCM}{tcn}[0000]{\gdef\MCM@opt@tcn{#1}}
\define@key{MCM}{problem}[A]{\gdef\MCM@opt@problem{#1}}
\define@key{MCM}{tstyle}[A]{\gdef\MCM@opt@tstyle{#1}}
\setkeys{MCM}{tcn=0000,problem=B,tstyle=\color{red}\bfseries}

\define@key{mcmthesis.cls}{tcn}[0000]{\gdef\MCM@opt@tcn{#1}}
\define@key{mcmthesis.cls}{problem}[A]{\gdef\MCM@opt@problem{#1}}
\define@key{mcmthesis.cls}{tstyle}[A]{\gdef\MCM@opt@tstyle{#1}}
\define@boolkey{mcmthesis.cls}[MCM@opt@]{CTeX}{}
\define@boolkey{mcmthesis.cls}[MCM@opt@]{titlepage}{}
\define@boolkey{mcmthesis.cls}[MCM@opt@]{abstract}{}
\define@boolkey{mcmthesis.cls}[MCM@opt@]{sheet}{}
\define@boolkey{mcmthesis.cls}[MCM@opt@]{titleinsheet}{}
\define@boolkey{mcmthesis.cls}[MCM@opt@]{keywordsinsheet}{}
\MCM@opt@sheettrue
\MCM@opt@titlepagetrue
\MCM@opt@titleinsheetfalse
\MCM@opt@keywordsinsheetfalse
\MCM@opt@abstracttrue
\newcommand{\mcmsetup}[1]{\setkeys{MCM}{#1}}
\ProcessOptionsX\relax
\LoadClass[letterpaper, 12pt]{article}
\newcommand{\team}{Team \#\ \MCM@opt@tcn}
\RequirePackage{fancyhdr, fancybox}
\RequirePackage{ifthen}
\RequirePackage{listings}
\RequirePackage[toc, page, title, titletoc, header]{appendix}
\RequirePackage{paralist}
\RequirePackage{amsthm, amsfonts}
\RequirePackage{amsmath, bm}
\RequirePackage{amssymb, mathrsfs}
\RequirePackage{latexsym}
\RequirePackage{longtable, multirow, hhline, tabularx, array}
\RequirePackage{flafter}
\RequirePackage{pifont, calc}
\RequirePackage{colortbl, booktabs}
\RequirePackage{geometry}
\RequirePackage{hyperref}
\RequirePackage{ifpdf, ifxetex}
\ifMCM@opt@CTeX
\else
  \RequirePackage{environ}
\fi
\ifpdf
  \RequirePackage{graphicx}
  \RequirePackage{epstopdf}
\else
  \ifxetex
    \RequirePackage{graphicx}
  \else
    \RequirePackage[dvipdfmx]{graphicx}
    \RequirePackage{bmpsize}
  \fi
\fi
\RequirePackage[svgnames]{xcolor}
\ifpdf
  \hypersetup{hidelinks}
\else
  \ifxetex
    \hypersetup{hidelinks}
  \else
    \hypersetup{dvipdfm, hidelinks}
  \fi
\fi
\geometry{letterpaper, margin = 1in}
\fancypagestyle{main}{
\fancyhf{}
\lhead{\small\sffamily \team}
\rhead{\small\sffamily Page \thepage\ of \pageref{LastPage}}
}
\pagestyle{main}

\fancypagestyle{aimain}{
\fancyhf{}
\lhead{\small\sffamily \team}
\rhead{\small\sffamily Page \thepage }
}
\setlength\parskip{.5\baselineskip}
\renewcommand\tableofcontents{%
    \centerline{\normalfont\Large\bfseries\sffamily\contentsname
        \@mkboth{%
           \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
    \vskip 5ex%
    \@starttoc{toc}%
    }
\setcounter{totalnumber}{4}
\setcounter{topnumber}{2}
\setcounter{bottomnumber}{2}
\renewcommand{\textfraction}{0.15}
\renewcommand{\topfraction}{0.85}
\renewcommand{\bottomfraction}{0.65}
\renewcommand{\floatpagefraction}{0.60}
\renewcommand{\figurename}{Figure}
\renewcommand{\tablename}{Table}
\graphicspath{{./}{./img/}{./fig/}{./image/}{./figure/}{./picture/}
            {./imgs/}{./figs/}{./images/}{./figures/}{./pictures/}}
\def\maketitle{%
  %\let\saved@thepage\thepage
  %\let\thepage\relax
  \ifMCM@opt@sheet
  \makesheet
  \fi
  \newpage
  \setcounter{page}{1}
  \pagestyle{fancy}
  \ifMCM@opt@titlepage
    \MCM@maketitle
  \fi
  \newpage
}
\def\abstractname{Summary}
\ifMCM@opt@CTeX
  \newbox\@abstract%
  \setbox\@abstract\hbox{}%
  \long\def\abstract{\bgroup\global\setbox\@abstract\vbox\bgroup\hsize\textwidth\leftskip1cm\rightskip1cm}%
  \def\endabstract{\egroup\egroup}%
  \def\make@abstract{%
    \begin{center}%
      \textbf{\abstractname}%
    \end{center}%
    \usebox\@abstract\par
  }
\else
  \RenewEnviron{abstract}{\xdef\@abstract{\expandonce\BODY}}
  \def\make@abstract{%
    \begin{center}%
      \textbf{\abstractname}%
    \end{center}%
    \@abstract\par
  }
\fi
\newenvironment{letter}[1]{%
      \par%
      \bgroup\parindent0pt%
      \begin{minipage}{5cm}
      \flushleft #1%
      \end{minipage}}
      {\egroup\smallskip}

\def\keywordsname{Keywords}
\ifMCM@opt@CTeX
  \newbox\@keywords
  \setbox\@keywords\hbox{}
  \def\keywords{\global\setbox\@keywords\vbox\bgroup\noindent\leftskip0cm}
  \def\endkeywords{\egroup}%
  \def\make@keywords{%
   \par\hskip.4cm\textbf{\keywordsname}: \usebox\@keywords\hfill\par
  }
\else
  \NewEnviron{keywords}{\xdef\@keywords{\expandonce\BODY}}
  \def\make@keywords{%
    \par\noindent\textbf{\keywordsname}:
    \@keywords\par
  }
\fi
\newcommand{\headset}{{\the\year}\\MCM/ICM\\Summary Sheet}
\newcommand{\problem}[1]{\mcmsetup{problem = #1}}
\def\makesheet{%
  \thispagestyle{empty}%
  \null%
  \vspace*{-5pc}%
  \begin{center}
  \begingroup
  \setlength{\parindent}{0pt}
     \begin{minipage}[t]{0.33\linewidth}
      \centering%
      \textbf{Problem Chosen}\\[0.7pc]
      {\Large \MCM@opt@tstyle {\MCM@opt@problem}}\\[2.8pc]
     \end{minipage}%
     \begin{minipage}[t]{0.33\linewidth}
      \centering%
      \textbf{\headset}%
     \end{minipage}%
     \begin{minipage}[t]{0.33\linewidth}
      \centering%
      \textbf{Team Control Number}\\[0.7pc]
      {\Large\MCM@opt@tstyle{\MCM@opt@tcn}}\\[2.8pc]
     \end{minipage}\par
  \rule{\linewidth}{1.5pt}
  \endgroup
  \vskip 5pt%
  \ifMCM@opt@titleinsheet
    \normalfont \LARGE \@title \par
  \fi
  \end{center}
\ifMCM@opt@keywordsinsheet
  \make@abstract
  \make@keywords
\else
  \make@abstract
\fi}
\newcommand{\MCM@maketitle}{%
  %\let\thepage\saved@thepage
  %\setcounter{page}{1}
  \begin{center}%
  \let \footnote \thanks%
  \pagestyle{fancy}%
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
  \par
  \vskip 1.5em%
  \ifMCM@opt@abstract%
    \make@abstract
    \make@keywords
  \fi%
}
\def\MCM@memoto{\relax}
\newcommand{\memoto}[1]{\gdef\MCM@memoto{#1}}
\def\MCM@memofrom{\relax}
\newcommand{\memofrom}[1]{\gdef\MCM@memofrom{#1}}
\def\MCM@memosubject{\relax}
\newcommand{\memosubject}[1]{\gdef\MCM@memosubject{#1}}
\def\MCM@memodate{\relax}
\newcommand{\memodate}[1]{\gdef\MCM@memodate{#1}}
\def\MCM@memologo{\relax}
\newcommand{\memologo}[1]{\gdef\MCM@memologo{\protect #1}}
\def\@letterheadaddress{\relax}
\newcommand{\lhaddress}[1]{\gdef\@letterheadaddress{#1}}
\newenvironment{memo}[1][Memorandum]{%
  \pagestyle{fancy}%
  \ifthenelse{\equal{\MCM@memologo}{\relax}}{%
    % without logo specified.
  }{%
    % with logo specified
    \begin{minipage}[t]{\columnwidth}%
      \begin{flushright}
        \vspace{-0.2in}
        \MCM@memologo
        \vspace{0.5in}
      \par\end{flushright}%
    \end{minipage}%
  }
  \begin{center}
    \LARGE\bfseries\scshape
    #1
  \end{center}
  \begin{description}
    \ifthenelse{\equal{\MCM@memoto}{\relax}}{}{\item [{To:}] \MCM@memoto}
    \ifthenelse{\equal{\MCM@memofrom}{\relax}}{}{\item [{From:}] \MCM@memofrom}
    \ifthenelse{\equal{\MCM@memosubject}{\relax}}{}{\item [{Subject:}] \MCM@memosubject}
    \ifthenelse{\equal{\MCM@memodate}{\relax}}{}{\item [{Date:}] \MCM@memodate}
  \end{description}
  \par\noindent
  \rule[0.5ex]{\linewidth}{0.1pt}\par
  \bigskip{}
}{%
  \clearpage
  \pagestyle{fancy}%
}
\newtheorem{Theorem}{Theorem}[section]
\newtheorem{Lemma}[Theorem]{Lemma}
\newtheorem{Corollary}[Theorem]{Corollary}
\newtheorem{Proposition}[Theorem]{Proposition}
\newtheorem{Definition}[Theorem]{Definition}
\newtheorem{Example}[Theorem]{Example}
\renewcommand\section{\@startsection{section}{1}{\z@}%
  {-1sp\@plus -.2ex \@minus -.2ex}%
  {1pt \@plus .2ex}%
  {\rmfamily\Large\bfseries}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
  {-1sp\@plus -.2ex \@minus -.2ex}%
  {1pt \@plus .2ex}%
  {\rmfamily\large\bfseries}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
  {-.5ex\@plus -1ex \@minus -.2ex}%
  {.25ex \@plus .2ex}%
  {\rmfamily\normalsize\bfseries}}
\renewcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
  {1ex \@plus1ex \@minus.2ex}%
  {-1em}%
  {\rmfamily\normalsize}}

\providecommand{\dif}{\mathop{}\!\mathrm{d}}
\providecommand{\me}{\mathrm{e}}
\providecommand{\mi}{\mathrm{i}}

\definecolor{grey}{rgb}{0.8,0.8,0.8}
\definecolor{darkgreen}{rgb}{0,0.3,0}
\definecolor{darkblue}{rgb}{0,0,0.3}
\def\lstbasicfont{\fontfamily{pcr}\selectfont\footnotesize}
\lstset{%
   % numbers=left,
   % numberstyle=\small,%
    showstringspaces=false,
    showspaces=false,%
    tabsize=4,%
    frame=lines,%
    basicstyle={\footnotesize\lstbasicfont},%
    keywordstyle=\color{darkblue}\bfseries,%
    identifierstyle=,%
    commentstyle=\color{darkgreen},%\itshape,%
    stringstyle=\color{black},%
    breaklines=true,%
    postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}
}
\lstloadlanguages{C,C++,Java,Matlab,python,Mathematica}


\def\AIcite{\@newl@bel b}
\let\citation\@gobble
\DeclareRobustCommand\AIcite{%
  \@ifnextchar [{\@tempswatrue\@AIcitex}{\@tempswafalse\@AIcitex[]}}
\def\@AIcitex[#1]#2{\leavevmode
  \let\@AIcitea\@empty
  \@AIcite{\@for\@AIciteb:=#2\do
    {\@AIcitea\def\@AIcitea{,\penalty\@m\ }%
     \edef\@AIciteb{\expandafter\@firstofone\@AIciteb\@empty}%
     \if@filesw\immediate\write\@auxout{\string\citation{\@AIciteb}}\fi
     \@ifundefined{b@\@AIciteb}{\hbox{\reset@font\bfseries ?}%
       \G@refundefinedtrue
       \@latex@warning
         {Citation `\@AIciteb' on page \thepage \space undefined}}%
       {\@AIcite@ofmt{\csname b@\@AIciteb\endcsname}}}}{#1}}
\def\@AIcite#1#2{[AI: {#1\if@tempswa , #2\fi}]}
\let\@AIcite@ofmt\hbox

\def\reportname{Report on Use of AI}

\providecommand\@AIlabel[1]{#1.~}

\newenvironment{ReportAiUse}[1]
     {\centerline{\underline{\large\sffamily\bfseries\reportname}}%
     \vspace*{-.2em}
      \@mkboth{\MakeUppercase\refname}{\MakeUppercase\refname}%
      \list{\@AIlabel{\@arabic\c@enumiv}}%
           {\settowidth\labelwidth{\@AIlabel{#1}}%
            \leftmargin\labelwidth
            \advance\leftmargin\labelsep
            \@openbib@code
            \usecounter{enumiv}%
            \let\p@enumiv\@empty
            \renewcommand\theenumiv{\@arabic\c@enumiv}}%
      \sloppy
      \clubpenalty4000
      \@clubpenalty \clubpenalty
      \widowpenalty4000%
      \sfcode`\.\@m}
     {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
      \endlist}
\def\AImatter{\label{LastPage}\clearpage\pagestyle{aimain}}
\endinput
%% 
%% This work consists of these files mcmthesis.dtx,
%%                                   figures/ and
%%                                   code/,
%% and the derived files             mcmthesis.cls,
%%                                   mcmthesis-demo.tex,
%%                                   README,
%%                                   LICENSE,
%%                                   mcmthesis.pdf and
%%                                   mcmthesis-demo.pdf.
%%
%% End of file `mcmthesis.cls'.

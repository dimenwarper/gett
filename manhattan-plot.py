


<!DOCTYPE html>
<html>
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# githubog: http://ogp.me/ns/fb/githubog#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>plots/manhattan-plot.py at master from brentp/bio-playground - GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />

    
    

    <meta content="authenticity_token" name="csrf-param" />
<meta content="qKcyWsKreyujhC6bYL4fSQEufH2EXz6ep7JbDQbWAJ4=" name="csrf-token" />

    <link href="https://a248.e.akamai.net/assets.github.com/stylesheets/bundles/github-af9e8cc9c66b3ec9725f21df4500f0f6093c9484.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="https://a248.e.akamai.net/assets.github.com/stylesheets/bundles/github2-39c4f2b2e1685cff3dd14e40d5a799c6fdddef8c.css" media="screen" rel="stylesheet" type="text/css" />
    

    <script src="https://a248.e.akamai.net/assets.github.com/javascripts/bundles/jquery-1ff4761a0d9866a948321eac8d969db3dc12938e.js" type="text/javascript"></script>
    <script src="https://a248.e.akamai.net/assets.github.com/javascripts/bundles/github-f18e47f6b8ff4e1edebdac2dc35b1ef0fb0eeae0.js" type="text/javascript"></script>
    

      <link rel='permalink' href='/brentp/bio-playground/blob/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a/plots/manhattan-plot.py'>
    <meta property="og:title" content="bio-playground"/>
    <meta property="og:type" content="githubog:gitrepository"/>
    <meta property="og:url" content="https://github.com/brentp/bio-playground"/>
    <meta property="og:image" content="https://a248.e.akamai.net/assets.github.com/images/gravatars/gravatar-140.png?1329275934"/>
    <meta property="og:site_name" content="GitHub"/>
    <meta property="og:description" content="bio-playground - miscellaneous scripts for bioinformatics/genomics that dont merit their own repo."/>

    <meta name="description" content="bio-playground - miscellaneous scripts for bioinformatics/genomics that dont merit their own repo." />
  <link href="https://github.com/brentp/bio-playground/commits/master.atom" rel="alternate" title="Recent Commits to bio-playground:master" type="application/atom+xml" />

  </head>


  <body class="logged_out page-blob  vis-public env-production ">
    


    

      <div id="header" class="true clearfix">
        <div class="container clearfix">
          <a class="site-logo" href="https://github.com">
            <!--[if IE]>
            <img alt="GitHub" class="github-logo" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7.png?1323882770" />
            <img alt="GitHub" class="github-logo-hover" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7-hover.png?1324325405" />
            <![endif]-->
            <img alt="GitHub" class="github-logo-4x" height="30" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7@4x.png?1323882770" />
            <img alt="GitHub" class="github-logo-4x-hover" height="30" src="https://a248.e.akamai.net/assets.github.com/images/modules/header/logov7@4x-hover.png?1324325405" />
          </a>

                  <!--
      make sure to use fully qualified URLs here since this nav
      is used on error pages on other domains
    -->
    <ul class="top-nav logged_out">
        <li class="pricing"><a href="https://github.com/plans">Signup and Pricing</a></li>
        <li class="explore"><a href="https://github.com/explore">Explore GitHub</a></li>
      <li class="features"><a href="https://github.com/features">Features</a></li>
        <li class="blog"><a href="https://github.com/blog">Blog</a></li>
      <li class="login"><a href="https://github.com/login?return_to=%2Fbrentp%2Fbio-playground%2Fblob%2Fmaster%2Fplots%2Fmanhattan-plot.py">Login</a></li>
    </ul>



          
        </div>
      </div>

      

            <div class="site">
      <div class="container">
        <div class="pagehead repohead instapaper_ignore readability-menu">
        <div class="title-actions-bar">
          <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
<a href="/brentp" itemprop="url">            <span itemprop="title">brentp</span>
            </a> /
            <strong><a href="/brentp/bio-playground" class="js-current-repository">bio-playground</a></strong>
          </h1>
          



              <ul class="pagehead-actions">


          <li><a href="/login?return_to=%2Fbrentp%2Fbio-playground" class="minibutton btn-watch watch-button entice tooltipped leftwards" rel="nofollow" title="You must be logged in to use this feature"><span><span class="icon"></span>Watch</span></a></li>
          <li><a href="/login?return_to=%2Fbrentp%2Fbio-playground" class="minibutton btn-fork fork-button entice tooltipped leftwards" rel="nofollow" title="You must be logged in to use this feature"><span><span class="icon"></span>Fork</span></a></li>


      <li class="repostats">
        <ul class="repo-stats">
          <li class="watchers ">
            <a href="/brentp/bio-playground/watchers" title="Watchers" class="tooltipped downwards">
              27
            </a>
          </li>
          <li class="forks">
            <a href="/brentp/bio-playground/network" title="Forks" class="tooltipped downwards">
              2
            </a>
          </li>
        </ul>
      </li>
    </ul>

        </div>

          

  <ul class="tabs">
    <li><a href="/brentp/bio-playground" class="selected" highlight="repo_sourcerepo_downloadsrepo_commitsrepo_tagsrepo_branches">Code</a></li>
    <li><a href="/brentp/bio-playground/network" highlight="repo_networkrepo_fork_queue">Network</a>
    <li><a href="/brentp/bio-playground/pulls" highlight="repo_pulls">Pull Requests <span class='counter'>0</span></a></li>

      <li><a href="/brentp/bio-playground/issues" highlight="repo_issues">Issues <span class='counter'>0</span></a></li>


    <li><a href="/brentp/bio-playground/graphs" highlight="repo_graphsrepo_contributors">Stats &amp; Graphs</a></li>

  </ul>

  
<div class="frame frame-center tree-finder" style="display:none"
      data-tree-list-url="/brentp/bio-playground/tree-list/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a"
      data-blob-url-prefix="/brentp/bio-playground/blob/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a"
    >

  <div class="breadcrumb">
    <span class="bold"><a href="/brentp/bio-playground">bio-playground</a></span> /
    <input class="tree-finder-input js-navigation-enable" type="text" name="query" autocomplete="off" spellcheck="false">
  </div>

    <div class="octotip">
      <p>
        <a href="/brentp/bio-playground/dismiss-tree-finder-help" class="dismiss js-dismiss-tree-list-help" title="Hide this notice forever" rel="nofollow">Dismiss</a>
        <span class="bold">Octotip:</span> You've activated the <em>file finder</em>
        by pressing <span class="kbd">t</span> Start typing to filter the
        file list. Use <span class="kbd badmono">↑</span> and
        <span class="kbd badmono">↓</span> to navigate,
        <span class="kbd">enter</span> to view files.
      </p>
    </div>

  <table class="tree-browser" cellpadding="0" cellspacing="0">
    <tr class="js-header"><th>&nbsp;</th><th>name</th></tr>
    <tr class="js-no-results no-results" style="display: none">
      <th colspan="2">No matching files</th>
    </tr>
    <tbody class="js-results-list js-navigation-container">
    </tbody>
  </table>
</div>

<div id="jump-to-line" style="display:none">
  <h2>Jump to Line</h2>
  <form>
    <input class="textfield" type="text">
    <div class="full-button">
      <button type="submit" class="classy">
        <span>Go</span>
      </button>
    </div>
  </form>
</div>


<div class="subnav-bar">

  <ul class="actions subnav">
    <li><a href="/brentp/bio-playground/tags" class="blank" highlight="repo_tags">Tags <span class="counter">0</span></a></li>
    <li><a href="/brentp/bio-playground/downloads" class="blank downloads-blank" highlight="repo_downloads">Downloads <span class="counter">0</span></a></li>
    
  </ul>

  <ul class="scope">
    <li class="switcher">

      <div class="context-menu-container js-menu-container">
        <a href="#"
           class="minibutton bigger switcher js-menu-target js-commitish-button btn-branch repo-tree"
           data-master-branch="master"
           data-ref="master">
          <span><span class="icon"></span><i>branch:</i> master</span>
        </a>

        <div class="context-pane commitish-context js-menu-content">
          <a href="javascript:;" class="close js-menu-close"></a>
          <div class="context-title">Switch Branches/Tags</div>
          <div class="context-body pane-selector commitish-selector js-filterable-commitishes">
            <div class="filterbar">
              <div class="placeholder-field js-placeholder-field">
                <label class="placeholder" for="context-commitish-filter-field" data-placeholder-mode="sticky">Filter branches/tags</label>
                <input type="text" id="context-commitish-filter-field" class="commitish-filter" />
              </div>

              <ul class="tabs">
                <li><a href="#" data-filter="branches" class="selected">Branches</a></li>
                <li><a href="#" data-filter="tags">Tags</a></li>
              </ul>
            </div>

              <div class="commitish-item branch-commitish selector-item">
                <h4>
                    <a href="/brentp/bio-playground/blob/master/plots/manhattan-plot.py" data-name="master" rel="nofollow">master</a>
                </h4>
              </div>


            <div class="no-results" style="display:none">Nothing to show</div>
          </div>
        </div><!-- /.commitish-context-context -->
      </div>

    </li>
  </ul>

  <ul class="subnav with-scope">

    <li><a href="/brentp/bio-playground" class="selected" highlight="repo_source">Files</a></li>
    <li><a href="/brentp/bio-playground/commits/master" highlight="repo_commits">Commits</a></li>
    <li><a href="/brentp/bio-playground/branches" class="" highlight="repo_branches" rel="nofollow">Branches <span class="counter">1</span></a></li>
  </ul>

</div>

  
  
  


          

        </div><!-- /.repohead -->

        




  
  <p class="last-commit">Latest commit to the <strong>master</strong> branch</p>

<div class="commit commit-tease js-details-container">
  <p class="commit-title ">
      <a href="/brentp/bio-playground/commit/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a" class="message">change column header to reflect relative location</a>
      
  </p>
  <div class="commit-meta">
    <a href="/brentp/bio-playground/commit/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a" class="sha-block">commit <span class="sha">aeb846d94e</span></a>
    <span class="js-clippy clippy-button " data-clipboard-text="aeb846d94e32fb28909ba5fa9ee76aa8772fca6a" data-copied-hint="copied!" data-copy-hint="Copy SHA"></span>

    <div class="authorship">
      <img class="gravatar" height="20" src="https://secure.gravatar.com/avatar/673a112cceaf8a4714ac6c3b6ae91690?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png" width="20" />
      <span class="author-name"><a href="/brentp">brentp</a></span>
      authored <time class="js-relative-date" datetime="2012-01-21T15:39:49-08:00" title="2012-01-21 15:39:49">January 21, 2012</time>

    </div>
  </div>
</div>


<!-- block_view_fragment_key: views4/v8/blob:v17:e065ba5311595f48921c11576be0130c -->
  <div id="slider">

    <div class="breadcrumb" data-path="plots/manhattan-plot.py/">
      <b itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/brentp/bio-playground/tree/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a" class="js-rewrite-sha" itemprop="url"><span itemprop="title">bio-playground</span></a></b> / <span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/brentp/bio-playground/tree/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a/plots" class="js-rewrite-sha" itemscope="url"><span itemprop="title">plots</span></a></span> / manhattan-plot.py <span class="js-clippy clippy-button " data-clipboard-text="plots/manhattan-plot.py" data-copied-hint="copied!" data-copy-hint="copy to clipboard"></span>
    </div>

    <div class="frames">
      <div class="frame frame-center" data-path="plots/manhattan-plot.py/" data-permalink-url="/brentp/bio-playground/blob/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a/plots/manhattan-plot.py" data-title="plots/manhattan-plot.py at master from brentp/bio-playground - GitHub" data-type="blob">
          <ul class="big-actions">
            <li><a class="file-edit-link minibutton js-rewrite-sha" href="/brentp/bio-playground/edit/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a/plots/manhattan-plot.py" data-method="post" rel="nofollow"><span>Edit this file</span></a></li>
          </ul>

        <div id="files" class="bubble">
          <div class="file">
            <div class="meta">
              <div class="info">
                <span class="icon"><img alt="Txt" height="16" src="https://a248.e.akamai.net/assets.github.com/images/icons/txt.png?1315937721" width="16" /></span>
                <span class="mode" title="File Mode">100644</span>
                  <span>130 lines (101 sloc)</span>
                <span>4.147 kb</span>
              </div>
              <ul class="actions">
                <li><a href="/brentp/bio-playground/raw/master/plots/manhattan-plot.py" id="raw-url">raw</a></li>
                  <li><a href="/brentp/bio-playground/blame/master/plots/manhattan-plot.py">blame</a></li>
                <li><a href="/brentp/bio-playground/commits/master/plots/manhattan-plot.py" rel="nofollow">history</a></li>
              </ul>
            </div>
              <div class="data type-python">
      <table cellpadding="0" cellspacing="0" class="lines">
        <tr>
          <td>
            <pre class="line_numbers"><span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>
<span id="L43" rel="#L43">43</span>
<span id="L44" rel="#L44">44</span>
<span id="L45" rel="#L45">45</span>
<span id="L46" rel="#L46">46</span>
<span id="L47" rel="#L47">47</span>
<span id="L48" rel="#L48">48</span>
<span id="L49" rel="#L49">49</span>
<span id="L50" rel="#L50">50</span>
<span id="L51" rel="#L51">51</span>
<span id="L52" rel="#L52">52</span>
<span id="L53" rel="#L53">53</span>
<span id="L54" rel="#L54">54</span>
<span id="L55" rel="#L55">55</span>
<span id="L56" rel="#L56">56</span>
<span id="L57" rel="#L57">57</span>
<span id="L58" rel="#L58">58</span>
<span id="L59" rel="#L59">59</span>
<span id="L60" rel="#L60">60</span>
<span id="L61" rel="#L61">61</span>
<span id="L62" rel="#L62">62</span>
<span id="L63" rel="#L63">63</span>
<span id="L64" rel="#L64">64</span>
<span id="L65" rel="#L65">65</span>
<span id="L66" rel="#L66">66</span>
<span id="L67" rel="#L67">67</span>
<span id="L68" rel="#L68">68</span>
<span id="L69" rel="#L69">69</span>
<span id="L70" rel="#L70">70</span>
<span id="L71" rel="#L71">71</span>
<span id="L72" rel="#L72">72</span>
<span id="L73" rel="#L73">73</span>
<span id="L74" rel="#L74">74</span>
<span id="L75" rel="#L75">75</span>
<span id="L76" rel="#L76">76</span>
<span id="L77" rel="#L77">77</span>
<span id="L78" rel="#L78">78</span>
<span id="L79" rel="#L79">79</span>
<span id="L80" rel="#L80">80</span>
<span id="L81" rel="#L81">81</span>
<span id="L82" rel="#L82">82</span>
<span id="L83" rel="#L83">83</span>
<span id="L84" rel="#L84">84</span>
<span id="L85" rel="#L85">85</span>
<span id="L86" rel="#L86">86</span>
<span id="L87" rel="#L87">87</span>
<span id="L88" rel="#L88">88</span>
<span id="L89" rel="#L89">89</span>
<span id="L90" rel="#L90">90</span>
<span id="L91" rel="#L91">91</span>
<span id="L92" rel="#L92">92</span>
<span id="L93" rel="#L93">93</span>
<span id="L94" rel="#L94">94</span>
<span id="L95" rel="#L95">95</span>
<span id="L96" rel="#L96">96</span>
<span id="L97" rel="#L97">97</span>
<span id="L98" rel="#L98">98</span>
<span id="L99" rel="#L99">99</span>
<span id="L100" rel="#L100">100</span>
<span id="L101" rel="#L101">101</span>
<span id="L102" rel="#L102">102</span>
<span id="L103" rel="#L103">103</span>
<span id="L104" rel="#L104">104</span>
<span id="L105" rel="#L105">105</span>
<span id="L106" rel="#L106">106</span>
<span id="L107" rel="#L107">107</span>
<span id="L108" rel="#L108">108</span>
<span id="L109" rel="#L109">109</span>
<span id="L110" rel="#L110">110</span>
<span id="L111" rel="#L111">111</span>
<span id="L112" rel="#L112">112</span>
<span id="L113" rel="#L113">113</span>
<span id="L114" rel="#L114">114</span>
<span id="L115" rel="#L115">115</span>
<span id="L116" rel="#L116">116</span>
<span id="L117" rel="#L117">117</span>
<span id="L118" rel="#L118">118</span>
<span id="L119" rel="#L119">119</span>
<span id="L120" rel="#L120">120</span>
<span id="L121" rel="#L121">121</span>
<span id="L122" rel="#L122">122</span>
<span id="L123" rel="#L123">123</span>
<span id="L124" rel="#L124">124</span>
<span id="L125" rel="#L125">125</span>
<span id="L126" rel="#L126">126</span>
<span id="L127" rel="#L127">127</span>
<span id="L128" rel="#L128">128</span>
<span id="L129" rel="#L129">129</span>
</pre>
          </td>
          <td width="100%">
                <div class="highlight"><pre><div class='line' id='LC1'><span class="sd">&quot;&quot;&quot;</span></div><div class='line' id='LC2'><span class="sd">    %prog [options] files</span></div><div class='line' id='LC3'><br/></div><div class='line' id='LC4'><span class="sd">plot a manhattan plot of the input file(s).</span></div><div class='line' id='LC5'><span class="sd">&quot;&quot;&quot;</span></div><div class='line' id='LC6'><br/></div><div class='line' id='LC7'><span class="kn">import</span> <span class="nn">optparse</span></div><div class='line' id='LC8'><span class="kn">import</span> <span class="nn">sys</span></div><div class='line' id='LC9'><span class="kn">from</span> <span class="nn">itertools</span> <span class="kn">import</span> <span class="n">groupby</span><span class="p">,</span> <span class="n">cycle</span></div><div class='line' id='LC10'><span class="kn">from</span> <span class="nn">operator</span> <span class="kn">import</span> <span class="n">itemgetter</span></div><div class='line' id='LC11'><span class="kn">from</span> <span class="nn">matplotlib</span> <span class="kn">import</span> <span class="n">pyplot</span> <span class="k">as</span> <span class="n">plt</span></div><div class='line' id='LC12'><span class="kn">import</span> <span class="nn">numpy</span> <span class="kn">as</span> <span class="nn">np</span></div><div class='line' id='LC13'><br/></div><div class='line' id='LC14'><span class="k">def</span> <span class="nf">_gen_data</span><span class="p">(</span><span class="n">fhs</span><span class="p">,</span> <span class="n">columns</span><span class="p">,</span> <span class="n">sep</span><span class="p">):</span></div><div class='line' id='LC15'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;</span></div><div class='line' id='LC16'><span class="sd">    iterate over the files and yield chr, start, pvalue</span></div><div class='line' id='LC17'><span class="sd">    &quot;&quot;&quot;</span></div><div class='line' id='LC18'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="n">fh</span> <span class="ow">in</span> <span class="n">fhs</span><span class="p">:</span></div><div class='line' id='LC19'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="n">line</span> <span class="ow">in</span> <span class="n">fh</span><span class="p">:</span></div><div class='line' id='LC20'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">line</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">==</span> <span class="s">&quot;#&quot;</span><span class="p">:</span> <span class="k">continue</span></div><div class='line' id='LC21'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">toks</span> <span class="o">=</span> <span class="n">line</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="n">sep</span><span class="p">)</span></div><div class='line' id='LC22'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">yield</span> <span class="n">toks</span><span class="p">[</span><span class="n">columns</span><span class="p">[</span><span class="mi">0</span><span class="p">]],</span> <span class="nb">int</span><span class="p">(</span><span class="n">toks</span><span class="p">[</span><span class="n">columns</span><span class="p">[</span><span class="mi">1</span><span class="p">]]),</span> <span class="nb">float</span><span class="p">(</span><span class="n">toks</span><span class="p">[</span><span class="n">columns</span><span class="p">[</span><span class="mi">2</span><span class="p">]])</span></div><div class='line' id='LC23'><br/></div><div class='line' id='LC24'><span class="k">def</span> <span class="nf">chr_cmp</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span></div><div class='line' id='LC25'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">a</span> <span class="o">=</span> <span class="n">a</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&quot;_&quot;</span><span class="p">,</span> <span class="s">&quot;&quot;</span><span class="p">);</span> <span class="n">b</span> <span class="o">=</span> <span class="n">b</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s">&quot;_&quot;</span><span class="p">,</span> <span class="s">&quot;&quot;</span><span class="p">)</span></div><div class='line' id='LC26'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">achr</span> <span class="o">=</span> <span class="n">a</span><span class="p">[</span><span class="mi">3</span><span class="p">:]</span> <span class="k">if</span> <span class="n">a</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="s">&quot;chr&quot;</span><span class="p">)</span> <span class="k">else</span> <span class="n">a</span></div><div class='line' id='LC27'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">bchr</span> <span class="o">=</span> <span class="n">b</span><span class="p">[</span><span class="mi">3</span><span class="p">:]</span> <span class="k">if</span> <span class="n">b</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="s">&quot;chr&quot;</span><span class="p">)</span> <span class="k">else</span> <span class="n">b</span></div><div class='line' id='LC28'><br/></div><div class='line' id='LC29'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">try</span><span class="p">:</span></div><div class='line' id='LC30'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nb">cmp</span><span class="p">(</span><span class="nb">int</span><span class="p">(</span><span class="n">achr</span><span class="p">),</span> <span class="nb">int</span><span class="p">(</span><span class="n">bchr</span><span class="p">))</span></div><div class='line' id='LC31'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">except</span> <span class="ne">ValueError</span><span class="p">:</span></div><div class='line' id='LC32'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">achr</span><span class="o">.</span><span class="n">isdigit</span><span class="p">()</span> <span class="ow">and</span> <span class="ow">not</span> <span class="n">bchr</span><span class="o">.</span><span class="n">isdigit</span><span class="p">():</span> <span class="k">return</span> <span class="o">-</span><span class="mi">1</span></div><div class='line' id='LC33'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">bchr</span><span class="o">.</span><span class="n">isdigit</span><span class="p">()</span> <span class="ow">and</span> <span class="ow">not</span> <span class="n">achr</span><span class="o">.</span><span class="n">isdigit</span><span class="p">():</span> <span class="k">return</span> <span class="mi">1</span></div><div class='line' id='LC34'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># X Y</span></div><div class='line' id='LC35'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nb">cmp</span><span class="p">(</span><span class="n">achr</span><span class="p">,</span> <span class="n">bchr</span><span class="p">)</span></div><div class='line' id='LC36'><br/></div><div class='line' id='LC37'><br/></div><div class='line' id='LC38'><span class="k">def</span> <span class="nf">chr_loc_cmp</span><span class="p">(</span><span class="n">alocs</span><span class="p">,</span> <span class="n">blocs</span><span class="p">):</span></div><div class='line' id='LC39'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">chr_cmp</span><span class="p">(</span><span class="n">alocs</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">blocs</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span> <span class="ow">or</span> <span class="nb">cmp</span><span class="p">(</span><span class="n">alocs</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="n">blocs</span><span class="p">[</span><span class="mi">1</span><span class="p">])</span></div><div class='line' id='LC40'><br/></div><div class='line' id='LC41'><br/></div><div class='line' id='LC42'><br/></div><div class='line' id='LC43'><span class="k">def</span> <span class="nf">manhattan</span><span class="p">(</span><span class="n">fhs</span><span class="p">,</span> <span class="n">columns</span><span class="p">,</span> <span class="n">image_path</span><span class="p">,</span> <span class="n">no_log</span><span class="p">,</span> <span class="n">colors</span><span class="p">,</span> <span class="n">sep</span><span class="p">,</span> <span class="n">title</span><span class="p">,</span> <span class="n">lines</span><span class="p">,</span> <span class="n">ymax</span><span class="p">):</span></div><div class='line' id='LC44'><br/></div><div class='line' id='LC45'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs</span> <span class="o">=</span> <span class="p">[]</span></div><div class='line' id='LC46'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ys</span> <span class="o">=</span> <span class="p">[]</span></div><div class='line' id='LC47'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cs</span> <span class="o">=</span> <span class="p">[]</span></div><div class='line' id='LC48'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">colors</span> <span class="o">=</span> <span class="n">cycle</span><span class="p">(</span><span class="n">colors</span><span class="p">)</span></div><div class='line' id='LC49'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs_by_chr</span> <span class="o">=</span> <span class="p">{}</span></div><div class='line' id='LC50'><br/></div><div class='line' id='LC51'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">last_x</span> <span class="o">=</span> <span class="mi">0</span></div><div class='line' id='LC52'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">data</span> <span class="o">=</span> <span class="nb">sorted</span><span class="p">(</span><span class="n">_gen_data</span><span class="p">(</span><span class="n">fhs</span><span class="p">,</span> <span class="n">columns</span><span class="p">,</span> <span class="n">sep</span><span class="p">),</span> <span class="nb">cmp</span><span class="o">=</span><span class="n">chr_loc_cmp</span><span class="p">)</span></div><div class='line' id='LC53'><br/></div><div class='line' id='LC54'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="n">seqid</span><span class="p">,</span> <span class="n">rlist</span> <span class="ow">in</span> <span class="n">groupby</span><span class="p">(</span><span class="n">data</span><span class="p">,</span> <span class="n">key</span><span class="o">=</span><span class="n">itemgetter</span><span class="p">(</span><span class="mi">0</span><span class="p">)):</span></div><div class='line' id='LC55'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">color</span> <span class="o">=</span> <span class="n">colors</span><span class="o">.</span><span class="n">next</span><span class="p">()</span></div><div class='line' id='LC56'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">rlist</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="n">rlist</span><span class="p">)</span></div><div class='line' id='LC57'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">region_xs</span> <span class="o">=</span> <span class="p">[</span><span class="n">last_x</span> <span class="o">+</span> <span class="n">r</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="k">for</span> <span class="n">r</span> <span class="ow">in</span> <span class="n">rlist</span><span class="p">]</span></div><div class='line' id='LC58'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs</span><span class="o">.</span><span class="n">extend</span><span class="p">(</span><span class="n">region_xs</span><span class="p">)</span></div><div class='line' id='LC59'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ys</span><span class="o">.</span><span class="n">extend</span><span class="p">([</span><span class="n">r</span><span class="p">[</span><span class="mi">2</span><span class="p">]</span> <span class="k">for</span> <span class="n">r</span> <span class="ow">in</span> <span class="n">rlist</span><span class="p">])</span></div><div class='line' id='LC60'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cs</span><span class="o">.</span><span class="n">extend</span><span class="p">([</span><span class="n">color</span><span class="p">]</span> <span class="o">*</span> <span class="nb">len</span><span class="p">(</span><span class="n">rlist</span><span class="p">))</span></div><div class='line' id='LC61'><br/></div><div class='line' id='LC62'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs_by_chr</span><span class="p">[</span><span class="n">seqid</span><span class="p">]</span> <span class="o">=</span> <span class="p">(</span><span class="n">region_xs</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">+</span> <span class="n">region_xs</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span> <span class="o">/</span> <span class="mi">2</span></div><div class='line' id='LC63'><br/></div><div class='line' id='LC64'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># keep track so that chrs don&#39;t overlap.</span></div><div class='line' id='LC65'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">last_x</span> <span class="o">=</span> <span class="n">xs</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span></div><div class='line' id='LC66'><br/></div><div class='line' id='LC67'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs_by_chr</span> <span class="o">=</span> <span class="p">[(</span><span class="n">k</span><span class="p">,</span> <span class="n">xs_by_chr</span><span class="p">[</span><span class="n">k</span><span class="p">])</span> <span class="k">for</span> <span class="n">k</span> <span class="ow">in</span> <span class="nb">sorted</span><span class="p">(</span><span class="n">xs_by_chr</span><span class="o">.</span><span class="n">keys</span><span class="p">(),</span> <span class="nb">cmp</span><span class="o">=</span><span class="n">chr_cmp</span><span class="p">)]</span></div><div class='line' id='LC68'><br/></div><div class='line' id='LC69'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">xs</span><span class="p">)</span></div><div class='line' id='LC70'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ys</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">ys</span><span class="p">)</span> <span class="k">if</span> <span class="n">no_log</span> <span class="k">else</span> <span class="o">-</span><span class="n">np</span><span class="o">.</span><span class="n">log10</span><span class="p">(</span><span class="n">ys</span><span class="p">)</span></div><div class='line' id='LC71'><br/></div><div class='line' id='LC72'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">plt</span><span class="o">.</span><span class="n">close</span><span class="p">()</span></div><div class='line' id='LC73'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">f</span> <span class="o">=</span> <span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">()</span></div><div class='line' id='LC74'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ax</span> <span class="o">=</span> <span class="n">f</span><span class="o">.</span><span class="n">add_axes</span><span class="p">((</span><span class="mf">0.1</span><span class="p">,</span> <span class="mf">0.09</span><span class="p">,</span> <span class="mf">0.88</span><span class="p">,</span> <span class="mf">0.85</span><span class="p">))</span></div><div class='line' id='LC75'><br/></div><div class='line' id='LC76'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">title</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></div><div class='line' id='LC77'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">plt</span><span class="o">.</span><span class="n">title</span><span class="p">(</span><span class="n">title</span><span class="p">)</span></div><div class='line' id='LC78'><br/></div><div class='line' id='LC79'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ax</span><span class="o">.</span><span class="n">set_ylabel</span><span class="p">(</span><span class="s">&#39;-log10(p-value)&#39;</span><span class="p">)</span></div><div class='line' id='LC80'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">lines</span><span class="p">:</span></div><div class='line' id='LC81'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ax</span><span class="o">.</span><span class="n">vlines</span><span class="p">(</span><span class="n">xs</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="n">ys</span><span class="p">,</span> <span class="n">colors</span><span class="o">=</span><span class="n">cs</span><span class="p">,</span> <span class="n">alpha</span><span class="o">=</span><span class="mf">0.5</span><span class="p">)</span></div><div class='line' id='LC82'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">else</span><span class="p">:</span></div><div class='line' id='LC83'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ax</span><span class="o">.</span><span class="n">scatter</span><span class="p">(</span><span class="n">xs</span><span class="p">,</span> <span class="n">ys</span><span class="p">,</span> <span class="n">s</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">c</span><span class="o">=</span><span class="n">cs</span><span class="p">,</span> <span class="n">alpha</span><span class="o">=</span><span class="mf">0.8</span><span class="p">,</span> <span class="n">edgecolors</span><span class="o">=</span><span class="s">&#39;none&#39;</span><span class="p">)</span></div><div class='line' id='LC84'><br/></div><div class='line' id='LC85'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># plot 0.05 line after multiple testing.</span></div><div class='line' id='LC86'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ax</span><span class="o">.</span><span class="n">axhline</span><span class="p">(</span><span class="n">y</span><span class="o">=-</span><span class="n">np</span><span class="o">.</span><span class="n">log10</span><span class="p">(</span><span class="mf">0.05</span> <span class="o">/</span> <span class="nb">len</span><span class="p">(</span><span class="n">data</span><span class="p">)),</span> <span class="n">color</span><span class="o">=</span><span class="s">&#39;0.5&#39;</span><span class="p">,</span> <span class="n">linewidth</span><span class="o">=</span><span class="mi">2</span><span class="p">)</span></div><div class='line' id='LC87'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">plt</span><span class="o">.</span><span class="n">axis</span><span class="p">(</span><span class="s">&#39;tight&#39;</span><span class="p">)</span></div><div class='line' id='LC88'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">plt</span><span class="o">.</span><span class="n">xlim</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">xs</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span></div><div class='line' id='LC89'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">plt</span><span class="o">.</span><span class="n">ylim</span><span class="p">(</span><span class="n">ymin</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span></div><div class='line' id='LC90'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">ymax</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span> <span class="n">plt</span><span class="o">.</span><span class="n">ylim</span><span class="p">(</span><span class="n">ymax</span><span class="o">=</span><span class="n">ymax</span><span class="p">)</span></div><div class='line' id='LC91'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">plt</span><span class="o">.</span><span class="n">xticks</span><span class="p">([</span><span class="n">c</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="k">for</span> <span class="n">c</span> <span class="ow">in</span> <span class="n">xs_by_chr</span><span class="p">],</span> <span class="p">[</span><span class="n">c</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="k">for</span> <span class="n">c</span> <span class="ow">in</span> <span class="n">xs_by_chr</span><span class="p">],</span> <span class="n">rotation</span><span class="o">=-</span><span class="mi">90</span><span class="p">,</span> <span class="n">size</span><span class="o">=</span><span class="mf">8.5</span><span class="p">)</span></div><div class='line' id='LC92'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">print</span> <span class="o">&gt;&gt;</span><span class="n">sys</span><span class="o">.</span><span class="n">stderr</span><span class="p">,</span> <span class="s">&quot;saving to: </span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="n">image_path</span></div><div class='line' id='LC93'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">plt</span><span class="o">.</span><span class="n">savefig</span><span class="p">(</span><span class="n">image_path</span><span class="p">)</span></div><div class='line' id='LC94'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c">#plt.show()</span></div><div class='line' id='LC95'><br/></div><div class='line' id='LC96'><br/></div><div class='line' id='LC97'><span class="k">def</span> <span class="nf">get_filehandles</span><span class="p">(</span><span class="n">args</span><span class="p">):</span></div><div class='line' id='LC98'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="p">(</span><span class="nb">open</span><span class="p">(</span><span class="n">a</span><span class="p">)</span> <span class="k">if</span> <span class="n">a</span> <span class="o">!=</span> <span class="s">&quot;-&quot;</span> <span class="k">else</span> <span class="n">sys</span><span class="o">.</span><span class="n">stdin</span> <span class="k">for</span> <span class="n">a</span> <span class="ow">in</span> <span class="n">args</span><span class="p">)</span></div><div class='line' id='LC99'><br/></div><div class='line' id='LC100'><br/></div><div class='line' id='LC101'><span class="k">def</span> <span class="nf">main</span><span class="p">():</span></div><div class='line' id='LC102'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">p</span> <span class="o">=</span> <span class="n">optparse</span><span class="o">.</span><span class="n">OptionParser</span><span class="p">(</span><span class="n">__doc__</span><span class="p">)</span></div><div class='line' id='LC103'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">p</span><span class="o">.</span><span class="n">add_option</span><span class="p">(</span><span class="s">&quot;--no-log&quot;</span><span class="p">,</span> <span class="n">dest</span><span class="o">=</span><span class="s">&quot;no_log&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s">&quot;don&#39;t do -log10(p) on the value&quot;</span><span class="p">,</span></div><div class='line' id='LC104'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">action</span><span class="o">=</span><span class="s">&#39;store_true&#39;</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="bp">False</span><span class="p">)</span></div><div class='line' id='LC105'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">p</span><span class="o">.</span><span class="n">add_option</span><span class="p">(</span><span class="s">&quot;--cols&quot;</span><span class="p">,</span> <span class="n">dest</span><span class="o">=</span><span class="s">&quot;cols&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s">&quot;zero-based column indexes to get&quot;</span></div><div class='line' id='LC106'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; chr, position, p-value respectively e.g. </span><span class="si">%d</span><span class="s">efault&quot;</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="s">&quot;0,1,2&quot;</span><span class="p">)</span></div><div class='line' id='LC107'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">p</span><span class="o">.</span><span class="n">add_option</span><span class="p">(</span><span class="s">&quot;--colors&quot;</span><span class="p">,</span> <span class="n">dest</span><span class="o">=</span><span class="s">&quot;colors&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s">&quot;cycle through these colors&quot;</span><span class="p">,</span></div><div class='line' id='LC108'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">default</span><span class="o">=</span><span class="s">&quot;bk&quot;</span><span class="p">)</span></div><div class='line' id='LC109'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">p</span><span class="o">.</span><span class="n">add_option</span><span class="p">(</span><span class="s">&quot;--image&quot;</span><span class="p">,</span> <span class="n">dest</span><span class="o">=</span><span class="s">&quot;image&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s">&quot;save the image to this file. e.g. </span><span class="si">%d</span><span class="s">efault&quot;</span><span class="p">,</span></div><div class='line' id='LC110'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">default</span><span class="o">=</span><span class="s">&quot;manhattan.png&quot;</span><span class="p">)</span></div><div class='line' id='LC111'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">p</span><span class="o">.</span><span class="n">add_option</span><span class="p">(</span><span class="s">&quot;--title&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s">&quot;title for the image.&quot;</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">dest</span><span class="o">=</span><span class="s">&quot;title&quot;</span><span class="p">)</span></div><div class='line' id='LC112'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">p</span><span class="o">.</span><span class="n">add_option</span><span class="p">(</span><span class="s">&quot;--ymax&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s">&quot;max (logged) y-value for plot&quot;</span><span class="p">,</span> <span class="n">dest</span><span class="o">=</span><span class="s">&quot;ymax&quot;</span><span class="p">,</span> <span class="nb">type</span><span class="o">=</span><span class="s">&#39;float&#39;</span><span class="p">)</span></div><div class='line' id='LC113'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">p</span><span class="o">.</span><span class="n">add_option</span><span class="p">(</span><span class="s">&quot;--sep&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s">&quot;data separator, default is [tab]&quot;</span><span class="p">,</span></div><div class='line' id='LC114'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">default</span><span class="o">=</span><span class="s">&quot;</span><span class="se">\t</span><span class="s">&quot;</span><span class="p">,</span> <span class="n">dest</span><span class="o">=</span><span class="s">&quot;sep&quot;</span><span class="p">)</span></div><div class='line' id='LC115'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">p</span><span class="o">.</span><span class="n">add_option</span><span class="p">(</span><span class="s">&quot;--lines&quot;</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="bp">False</span><span class="p">,</span> <span class="n">dest</span><span class="o">=</span><span class="s">&quot;lines&quot;</span><span class="p">,</span> <span class="n">action</span><span class="o">=</span><span class="s">&quot;store_true&quot;</span><span class="p">,</span></div><div class='line' id='LC116'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">help</span><span class="o">=</span><span class="s">&quot;plot the p-values as lines extending from the x-axis rather than&quot;</span></div><div class='line' id='LC117'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&quot; points in space. plotting will take longer with this option.&quot;</span><span class="p">)</span></div><div class='line' id='LC118'><br/></div><div class='line' id='LC119'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">opts</span><span class="p">,</span> <span class="n">args</span> <span class="o">=</span> <span class="n">p</span><span class="o">.</span><span class="n">parse_args</span><span class="p">()</span></div><div class='line' id='LC120'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">args</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><span class="p">):</span></div><div class='line' id='LC121'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sys</span><span class="o">.</span><span class="n">exit</span><span class="p">(</span><span class="ow">not</span> <span class="n">p</span><span class="o">.</span><span class="n">print_help</span><span class="p">())</span></div><div class='line' id='LC122'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">fhs</span> <span class="o">=</span> <span class="n">get_filehandles</span><span class="p">(</span><span class="n">args</span><span class="p">)</span></div><div class='line' id='LC123'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">columns</span> <span class="o">=</span> <span class="nb">map</span><span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="n">opts</span><span class="o">.</span><span class="n">cols</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s">&quot;,&quot;</span><span class="p">))</span></div><div class='line' id='LC124'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">manhattan</span><span class="p">(</span><span class="n">fhs</span><span class="p">,</span> <span class="n">columns</span><span class="p">,</span> <span class="n">opts</span><span class="o">.</span><span class="n">image</span><span class="p">,</span> <span class="n">opts</span><span class="o">.</span><span class="n">no_log</span><span class="p">,</span> <span class="n">opts</span><span class="o">.</span><span class="n">colors</span><span class="p">,</span> <span class="n">opts</span><span class="o">.</span><span class="n">sep</span><span class="p">,</span></div><div class='line' id='LC125'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">opts</span><span class="o">.</span><span class="n">title</span><span class="p">,</span> <span class="n">opts</span><span class="o">.</span><span class="n">lines</span><span class="p">,</span> <span class="n">opts</span><span class="o">.</span><span class="n">ymax</span><span class="p">)</span></div><div class='line' id='LC126'><br/></div><div class='line' id='LC127'><br/></div><div class='line' id='LC128'><span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">&quot;__main__&quot;</span><span class="p">:</span></div><div class='line' id='LC129'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">main</span><span class="p">()</span></div></pre></div>
          </td>
        </tr>
      </table>
  </div>

          </div>
        </div>
      </div>
    </div>

  </div>

<div class="frame frame-loading" style="display:none;" data-tree-list-url="/brentp/bio-playground/tree-list/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a" data-blob-url-prefix="/brentp/bio-playground/blob/aeb846d94e32fb28909ba5fa9ee76aa8772fca6a">
  <img src="https://a248.e.akamai.net/assets.github.com/images/modules/ajax/big_spinner_336699.gif?1302750674" height="32" width="32">
</div>

      </div>
      <div class="context-overlay"></div>
    </div>


      <!-- footer -->
      <div id="footer" >
        
  <div class="upper_footer">
     <div class="container clearfix">

       <!--[if IE]><h4 id="blacktocat_ie">GitHub Links</h4><![endif]-->
       <![if !IE]><h4 id="blacktocat">GitHub Links</h4><![endif]>

       <ul class="footer_nav">
         <h4>GitHub</h4>
         <li><a href="https://github.com/about">About</a></li>
         <li><a href="https://github.com/blog">Blog</a></li>
         <li><a href="https://github.com/features">Features</a></li>
         <li><a href="https://github.com/contact">Contact &amp; Support</a></li>
         <li><a href="https://github.com/training">Training</a></li>
         <li><a href="http://enterprise.github.com/">GitHub Enterprise</a></li>
         <li><a href="http://status.github.com/">Site Status</a></li>
       </ul>

       <ul class="footer_nav">
         <h4>Tools</h4>
         <li><a href="http://get.gaug.es/">Gauges: Analyze web traffic</a></li>
         <li><a href="http://speakerdeck.com">Speaker Deck: Presentations</a></li>
         <li><a href="https://gist.github.com">Gist: Code snippets</a></li>
         <li><a href="http://mac.github.com/">GitHub for Mac</a></li>
         <li><a href="http://mobile.github.com/">Issues for iPhone</a></li>
         <li><a href="http://jobs.github.com/">Job Board</a></li>
       </ul>

       <ul class="footer_nav">
         <h4>Extras</h4>
         <li><a href="http://shop.github.com/">GitHub Shop</a></li>
         <li><a href="http://octodex.github.com/">The Octodex</a></li>
       </ul>

       <ul class="footer_nav">
         <h4>Documentation</h4>
         <li><a href="http://help.github.com/">GitHub Help</a></li>
         <li><a href="http://developer.github.com/">Developer API</a></li>
         <li><a href="http://github.github.com/github-flavored-markdown/">GitHub Flavored Markdown</a></li>
         <li><a href="http://pages.github.com/">GitHub Pages</a></li>
       </ul>

     </div><!-- /.site -->
  </div><!-- /.upper_footer -->

<div class="lower_footer">
  <div class="container clearfix">
    <!--[if IE]><div id="legal_ie"><![endif]-->
    <![if !IE]><div id="legal"><![endif]>
      <ul>
          <li><a href="https://github.com/site/terms">Terms of Service</a></li>
          <li><a href="https://github.com/site/privacy">Privacy</a></li>
          <li><a href="https://github.com/security">Security</a></li>
      </ul>

      <p>&copy; 2012 <span title="0.08134s from fe5.rs.github.com">GitHub</span> Inc. All rights reserved.</p>
    </div><!-- /#legal or /#legal_ie-->

      <div class="sponsor">
        <a href="http://www.rackspace.com" class="logo">
          <img alt="Dedicated Server" height="36" src="https://a248.e.akamai.net/assets.github.com/images/modules/footer/rackspaces_logo.png?1329521041" width="38" />
        </a>
        Powered by the <a href="http://www.rackspace.com ">Dedicated
        Servers</a> and<br/> <a href="http://www.rackspacecloud.com">Cloud
        Computing</a> of Rackspace Hosting<span>&reg;</span>
      </div>
  </div><!-- /.site -->
</div><!-- /.lower_footer -->

      </div><!-- /#footer -->

    

<div id="keyboard_shortcuts_pane" class="instapaper_ignore readability-extra" style="display:none">
  <h2>Keyboard Shortcuts <small><a href="#" class="js-see-all-keyboard-shortcuts">(see all)</a></small></h2>

  <div class="columns threecols">
    <div class="column first">
      <h3>Site wide shortcuts</h3>
      <dl class="keyboard-mappings">
        <dt>s</dt>
        <dd>Focus site search</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>?</dt>
        <dd>Bring up this help dialog</dd>
      </dl>
    </div><!-- /.column.first -->

    <div class="column middle" style='display:none'>
      <h3>Commit list</h3>
      <dl class="keyboard-mappings">
        <dt>j</dt>
        <dd>Move selection down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>k</dt>
        <dd>Move selection up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>c <em>or</em> o <em>or</em> enter</dt>
        <dd>Open commit</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>y</dt>
        <dd>Expand URL to its canonical form</dd>
      </dl>
    </div><!-- /.column.first -->

    <div class="column last" style='display:none'>
      <h3>Pull request list</h3>
      <dl class="keyboard-mappings">
        <dt>j</dt>
        <dd>Move selection down</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>k</dt>
        <dd>Move selection up</dd>
      </dl>
      <dl class="keyboard-mappings">
        <dt>o <em>or</em> enter</dt>
        <dd>Open issue</dd>
      </dl>
    </div><!-- /.columns.last -->

  </div><!-- /.columns.equacols -->

  <div style='display:none'>
    <div class="rule"></div>

    <h3>Issues</h3>

    <div class="columns threecols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt>j</dt>
          <dd>Move selection down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>k</dt>
          <dd>Move selection up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>x</dt>
          <dd>Toggle selection</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>o <em>or</em> enter</dt>
          <dd>Open issue</dd>
        </dl>
      </div><!-- /.column.first -->
      <div class="column middle">
        <dl class="keyboard-mappings">
          <dt>I</dt>
          <dd>Mark selection as read</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>U</dt>
          <dd>Mark selection as unread</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>e</dt>
          <dd>Close selection</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>y</dt>
          <dd>Remove selection from view</dd>
        </dl>
      </div><!-- /.column.middle -->
      <div class="column last">
        <dl class="keyboard-mappings">
          <dt>c</dt>
          <dd>Create issue</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>l</dt>
          <dd>Create label</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>i</dt>
          <dd>Back to inbox</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>u</dt>
          <dd>Back to issues</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>/</dt>
          <dd>Focus issues search</dd>
        </dl>
      </div>
    </div>
  </div>

  <div style='display:none'>
    <div class="rule"></div>

    <h3>Issues Dashboard</h3>

    <div class="columns threecols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt>j</dt>
          <dd>Move selection down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>k</dt>
          <dd>Move selection up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>o <em>or</em> enter</dt>
          <dd>Open issue</dd>
        </dl>
      </div><!-- /.column.first -->
    </div>
  </div>

  <div style='display:none'>
    <div class="rule"></div>

    <h3>Network Graph</h3>
    <div class="columns equacols">
      <div class="column first">
        <dl class="keyboard-mappings">
          <dt><span class="badmono">←</span> <em>or</em> h</dt>
          <dd>Scroll left</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="badmono">→</span> <em>or</em> l</dt>
          <dd>Scroll right</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="badmono">↑</span> <em>or</em> k</dt>
          <dd>Scroll up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt><span class="badmono">↓</span> <em>or</em> j</dt>
          <dd>Scroll down</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>t</dt>
          <dd>Toggle visibility of head labels</dd>
        </dl>
      </div><!-- /.column.first -->
      <div class="column last">
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">←</span> <em>or</em> shift h</dt>
          <dd>Scroll all the way left</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">→</span> <em>or</em> shift l</dt>
          <dd>Scroll all the way right</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">↑</span> <em>or</em> shift k</dt>
          <dd>Scroll all the way up</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>shift <span class="badmono">↓</span> <em>or</em> shift j</dt>
          <dd>Scroll all the way down</dd>
        </dl>
      </div><!-- /.column.last -->
    </div>
  </div>

  <div >
    <div class="rule"></div>
    <div class="columns threecols">
      <div class="column first" >
        <h3>Source Code Browsing</h3>
        <dl class="keyboard-mappings">
          <dt>t</dt>
          <dd>Activates the file finder</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>l</dt>
          <dd>Jump to line</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>w</dt>
          <dd>Switch branch/tag</dd>
        </dl>
        <dl class="keyboard-mappings">
          <dt>y</dt>
          <dd>Expand URL to its canonical form</dd>
        </dl>
      </div>
    </div>
  </div>
</div>

    <div id="markdown-help" class="instapaper_ignore readability-extra">
  <h2>Markdown Cheat Sheet</h2>

  <div class="cheatsheet-content">

  <div class="mod">
    <div class="col">
      <h3>Format Text</h3>
      <p>Headers</p>
      <pre>
# This is an &lt;h1&gt; tag
## This is an &lt;h2&gt; tag
###### This is an &lt;h6&gt; tag</pre>
     <p>Text styles</p>
     <pre>
*This text will be italic*
_This will also be italic_
**This text will be bold**
__This will also be bold__

*You **can** combine them*
</pre>
    </div>
    <div class="col">
      <h3>Lists</h3>
      <p>Unordered</p>
      <pre>
* Item 1
* Item 2
  * Item 2a
  * Item 2b</pre>
     <p>Ordered</p>
     <pre>
1. Item 1
2. Item 2
3. Item 3
   * Item 3a
   * Item 3b</pre>
    </div>
    <div class="col">
      <h3>Miscellaneous</h3>
      <p>Images</p>
      <pre>
![GitHub Logo](/images/logo.png)
Format: ![Alt Text](url)
</pre>
     <p>Links</p>
     <pre>
http://github.com - automatic!
[GitHub](http://github.com)</pre>
<p>Blockquotes</p>
     <pre>
As Kanye West said:

> We're living the future so
> the present is our past.
</pre>
    </div>
  </div>
  <div class="rule"></div>

  <h3>Code Examples in Markdown</h3>
  <div class="col">
      <p>Syntax highlighting with <a href="http://github.github.com/github-flavored-markdown/" title="GitHub Flavored Markdown" target="_blank">GFM</a></p>
      <pre>
```javascript
function fancyAlert(arg) {
  if(arg) {
    $.facebox({div:'#foo'})
  }
}
```</pre>
    </div>
    <div class="col">
      <p>Or, indent your code 4 spaces</p>
      <pre>
Here is a Python code example
without syntax highlighting:

    def foo:
      if not bar:
        return true</pre>
    </div>
    <div class="col">
      <p>Inline code for comments</p>
      <pre>
I think you should use an
`&lt;addr&gt;` element here instead.</pre>
    </div>
  </div>

  </div>
</div>


    <div class="ajax-error-message">
      <p><span class="icon"></span> Something went wrong with that request. Please try again. <a href="javascript:;" class="ajax-error-dismiss">Dismiss</a></p>
    </div>

    
    
    
    <span id='server_response_time' data-time='0.08707' data-host='fe5'></span>
  </body>
</html>


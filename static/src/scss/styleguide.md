<div class="container-fluid">
    <div class="flex flex-right hidden-lg-down">                    
        <small class="text-muted half-margin-top">Version 2.0.1</small>
    </div>
    <div class="section section--loose">
        <div class="row">
            <div class="col-md-4 col-lg-3 offset-lg-1 col-xl-2 offset-xl-1 fixed-left-xl-up">
                <div id="mobilehome" class="form-group dropdown hidden-md-up ignore">
                    <div class="form-group__text select">
                        <input value="Select a Pattern">
                    </div>
                    <div class="dropdown__menu">
                        <a onclick="updateUrl('home')" id="mobilehome-home" tabindex="0">Overview</a>
                        <a onclick="updateUrl('designers')" id="mobilehome-designers" tabindex="0">For Designers</a>
                        <a onclick="updateUrl('gettingstarted')" id="mobilehome-gettingstarted" tabindex="0">Getting Started</a>
                        <a onclick="updateUrl('examples')" id="mobilehome-examples" tabindex="0">Examples</a>
                        <a onclick="updateUrl('releases')" id="mobilehome-releases" tabindex="0">Previous Releases</a>
                        <a onclick="updateUrl('migration')" id="mobilehome-migration" tabindex="0">Migration Guide</a>
                        <a onclick="updateUrl('changelog')" id="mobilehome-changelog" tabindex="0">Change Log</a>
                    </div>
                </div>
                <ul id="tabshome" class="tabs tabs--vertical hidden-sm-down">
                    <li id="tabshome-home" class="tab">
                        <a href="" tabindex="0">
                            <div class="tab__heading">Overview</div>
                        </a>
                    </li>
                    <li id="tabshome-designers" class="tab">
                        <a onclick="updateUrl('designers')" tabindex="0">
                            <div class="tab__heading">For Designers</div>
                        </a>
                    </li>
                    <li id="tabshome-gettingstarted" class="tab">
                        <a onclick="updateUrl('gettingstarted')" tabindex="0">
                            <div class="tab__heading">Getting Started</div>
                        </a>
                    </li>
                    <li id="tabshome-examples" class="tab">
                        <a onclick="updateUrl('examples')" tabindex="0">
                            <div class="tab__heading">Examples</div>
                        </a>
                    </li>
                    <li id="tabshome-releases" class="tab">
                        <a onclick="updateUrl('releases')" tabindex="0">
                            <div class="tab__heading">Previous Releases</div>
                        </a>
                    </li>
                    <li id="tabshome-migration" class="tab">
                        <a onclick="updateUrl('migration')" tabindex="0">
                            <div class="tab__heading">Migration Guide</div>
                        </a>
                    </li>
                    <li id="tabshome-changelog" class="tab">
                        <a onclick="updateUrl('changelog')" tabindex="0">
                            <div class="tab__heading">Change Log</div>
                        </a>
                    </li>
                </ul>
            </div>
            <div class="col-md-8 col-lg-7 col-xl-8 offset-xl-3">
                <div id="tabshome-content" class="tab-content">
                    <div id="tabshome-home-content" class="tab-pane">
                        <div class="row no-margin">
                            <div class="col-lg-12 col-xl-6">
                                <h1 class="display-0 display-3-md">Cisco UI Kit</h1>
                                <h5 class="subheading">A lightweight presentation layer sponsored by Cisco Brand and designed for web applications</h5>
                                <div class="section dbl-padding-top">
                                    <a class="btn btn--large btn--wide btn--primary" target="_blank" href="dist/cui-2.0.1-standard.zip">Download</a>
                                    <button class="btn btn--large btn--link" onclick="doTabChange('tabshome-gettingstarted');updateUrl('gettingstarted')">Learn More</button>
                                </div>
                            </div>
                            <div class="col-6 hidden-lg-down">
                                <div class="hex-gallery">
                                    <div class="hex-item">
                                        <a href="section-components.html#components-alert">
                                            <img src="public/img/alert-sampler.png">
                                            <div class="caption">Alert</div>
                                        </a>
                                    </div>
                                    <div class="hex-item">
                                        <a href="section-primitives.html#primitives-button">
                                            <img src="public/img/button-sampler.png">
                                            <div class="caption">Button</div>
                                        </a>
                                    </div>
                                    <div class="hex-item">
                                        <a href="section-primitives.html#primitives-checkbox">
                                            <img src="public/img/checkbox-sampler.png">
                                            <div class="caption">Checkbox</div>
                                        </a>
                                    </div>
                                    <div class="hex-item">
                                        <a href="section-primitives.html#primitives-icons">
                                            <img src="public/img/icon-sampler.png">
                                            <div class="caption">Icons</div>
                                        </a>
                                    </div>
                                    <div class="hex-item">
                                        <a href="section-components.html#components-dropdown">
                                            <img src="public/img/dropdown-sampler.png">
                                            <div class="caption">Dropdown</div>
                                        </a>
                                    </div>
                                    <div class="hex-item hex-label">
                                        <img src="public/img/uikit-web-apps.png">
                                        <div class="caption">30 Design Patterns</div>
                                    </div>
                                    <div class="hex-item">
                                        <a href="section-components.html#components-step">
                                            <img src="public/img/step-sampler.png">
                                            <div class="caption">Step</div>
                                        </a>
                                    </div>
                                    <div class="hex-item">
                                        <a href="section-components.html#components-timeline">
                                            <img src="public/img/timeline-sampler.png">
                                            <div class="caption">Timeline</div>
                                        </a>
                                    </div>
                                    <div class="hex-item">
                                        <a href="section-design.html#design-palette">
                                            <img src="public/img/palette-sampler.png">
                                            <div class="caption">Colors</div>
                                        </a>
                                    </div>
                                    <div class="hex-item">
                                        <a href="section-components.html#components-tLIst">
                                            <img src="public/img/toast-sampler.png">
                                            <div class="caption">Toast</div>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>                    
                    </div>
                    <div id="tabshome-designers-content" class="tab-pane">
                        <h1>For Designers</h1>
                        <div class="section">
                            <div class="row">
                                <div class="col-lg-4">
                                    <div class="panel panel--loose panel--raised motion-slide-in-top dbl-margin-bottom">
                                        <div class="row">
                                            <div class="col-xl-2 flex-center">
                                                <img src="public/img/sketch-logo-thumb.png">
                                            </div>
                                            <div class="col-xl-10">
                                                <h5>Sketch Symbols</h5>
                                                <p>Sketch library file containing all the patterns in this kit</p>
                                                <a href="https://cisco.box.com/shared/static/nswgmeaie6kuohncs0pt568g9akeb0md.sketch" download="https://cisco.box.com/shared/static/nswgmeaie6kuohncs0pt568g9akeb0md.sketch">
                                                    <span>download</span>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-lg-4">
                                    <div class="panel panel--loose panel--raised motion-slide-in-top dbl-margin-bottom">
                                        <div class="row">
                                            <div class="col-xl-2 flex-center">
                                                <img src="public/img/svg-logo-thumb.png">
                                            </div>
                                            <div class="col-xl-10">
                                                <h5>SVG Library</h5>
                                                <p>File containing all the patterns (as SVGs) in this kit</p>
                                                <a href="https://cisco.box.com/shared/static/sbwrdj32yomqytnabbe6jf41kah834hc.zip" download="https://cisco.box.com/shared/static/sbwrdj32yomqytnabbe6jf41kah834hc.zip">
                                                    <span>download</span>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-lg-4">
                                    <div class="panel panel--loose panel--raised motion-slide-in-top dbl-margin-bottom">
                                        <div class="row">
                                            <div class="col-xl-2 flex-center">
                                                <img src="public/img/icons-logo-thumb.png">
                                            </div>
                                            <div class="col-xl-10">
                                                <h5>Icon Library</h5>
                                                <p>File containing the full set of svg-based icons in this kit</p>
                                                <a href="https://cisco.box.com/shared/static/3ooooglymk2x3p7x1mjc5gp8byp7yxvr.zip" download="https://cisco.box.com/shared/static/3ooooglymk2x3p7x1mjc5gp8byp7yxvr.zip">
                                                    <span>download</span>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="tabshome-gettingstarted-content" class="tab-pane gettingstarted">
                        <h1>Getting Started</h1>
                        <p class="lead">Download, install and start using the UI kit.</p>
                        <div class="section">
                            <h3>Download</h3>
                            <p>There are multiple ways to get the UI kit:</p>
                            <ul>
                                <li><a target="_blank" href="dist/cui-2.0.1-standard.zip">Download</a> the pre-built CSS and font files.</li>
                                <li><a target="_blank" href="dist/cui-2.0.1-source.zip">Download</a> the uncompiled SCSS files, font files and icons.</li>
                                <li>
                                    <div>Clone the repo to get all the source files, pre-compiled CSS and font files. Run this from the command line.</div>
                                    <pre>
                                        <code class="code-raw" data-language="html">
git clone https://gitlab-sjc.cisco.com/cisco-ui/pattern-library.git
                                        </code>
                                    </pre>
                                </li>
                                <li>
                                    <div>Or add this line to your <i>package.json</i> file to pull it in via node package manager as part of npm install.</div>
                                    <pre>
                                        <code class="code-raw" data-language="html">
"cisco-ui": "git+ssh://git@gitlab-sjc.cisco.com:cisco-ui/pattern-library.git#2.0.1"
                                        </code>
                                    </pre>
                                <li>
                                    <div>Leverage the Cisco CDN. Your application can pull in the pre-built CSS directly from Cisco's content delivery network.</div>
                                    <pre>
                                        <code class="code-raw" data-language="html">
&lt;link href="http://www.cisco.com/web/fw/cisco-ui/2.0.1/dist/css/cui-standard.min.css" rel="stylesheet" type="text/css"&gt;
                                        </code>
                                    </pre>
                                </li>
                            </ul>
                        </div>
                        <div class="section">
                            <h3>Installation</h3>
                            <p>Once downloaded and unzipped, there are two additional steps to start using the UI kit in your application:</p>
                            <div class="steps steps--vertical steps--small">
                                <div class="step active">
                                    <div class="step__icon">1</div>
                                    <div class="step__label">
                                        <div>Pull the CSS into your application inside the head tag section. The CSS will pull in the font files based on relative folder structure. This means the `/font` folder should be a peer of the `/css` folder:</div>
                                        <pre>
                                            <code class="code-raw" data-language="html">
&lt;link href="css/cui-standard.min.css" rel="stylesheet" type="text/css"&gt;
                                            </code>
                                        </pre>
                                    </div>
                                </div>
                                <div class="step active">
                                    <div class="step__icon">2</div>
                                    <div class="step__label">
                                        <div>Now add the `cui` class to the body tag in your main application file:</div>
                                        <pre>
                                            <code class="code-raw" data-language="html">
&lt;body class="cui"&gt;...&lt;/body&gt;
                                            </code>
                                        </pre>
                                        <div>Finally, open up your favorite browser and point it to your main application file.</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="section">
                            <h3>Page Setup</h3>
                            <p>Some notes on setting up your page in terms of theme and width.</p>
                            <div class="subheader">Theme</div>
                            <div>The Dark theme is built into the existing UI kit CSS which means toggling it in your application is simple. Just add the theme attribute to your body tag like this:</div>
                            <pre>
                                <code class="code-raw" data-language="html">
&lt;body class="cui" data-theme="dark"&gt;...&lt;/body&gt;
                                </code>
                            </pre>
                            <img src="public/img/dark-example-thumb.png">
                            <hr>
                            <div class="subheader">Width</div>
                            <div>By default, the UI kit page bed is set at 1600px. The `container` class governs this max width. If your application needs a wider page bed (>1600px) then use `container-fluid`.</div>
                        </div>
                        <div class="section">
                            <h3>Component Libraries</h3>
                            <p>There are several internal open source teams within Cisco actively building components based on this kit:</p>
                            <ul>
                                <li><a href="http://swtg-rtp-dev-7/angular/" target="_blank">Angular UI NGX</a></li>
                                <li><a href="https://scripts.cisco.com/app/ReactCUI/#/" target="_blank">React UI</a></li>
                            </ul>
                        </div>
                        <div class="section">
                            <h3>Additional Information</h3>
                            <ul>
                                <li>You can post comments or ask questions in our WebEx Teamspace Cisco UI/UX Office Hours.</li>
                                <li>Access our Wiki <a href="https://apps.na.collabserv.com/communities/service/html/communitystart?communityUuid=f440dc5c-b623-4fdb-b5da-a455c5a1ac58" target="_blank">here</a></li>
                            </ul>
                        </div>
                    </div>
                    <div id="tabshome-examples-content" class="tab-pane">
                        <h1>Examples</h1>
                        <div class="section">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="motion-slide-in-top dbl-margin-bottom">
                                        <div class="row">
                                            <div class="col-6">
                                                <a href="assets/collage.html">
                                                    <img class="thumb" src="public/img/collage-example-thumb.png">
                                                </a>
                                            </div>
                                            <div class="col-6">
                                                <div class="subtitle">Collage</div>
                                                <p>All patterns in the kit on one page.</p>
                                                <a href="assets/collage.html">view</a>
                                                <div class="v-separator"></div>
                                                <a href="public/assets/collage.html" download="public/assets/collage.html">download</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="motion-slide-in-top dbl-margin-bottom">
                                        <div class="row">
                                            <div class="col-6">
                                                <a href="assets/list.html">
                                                    <img class="thumb" src="public/img/list-example-thumb.png">
                                                </a>
                                            </div>
                                            <div class="col-6">
                                                <div class="subtitle">List</div>
                                                <p>Sample list page showing table and pagination.</p>
                                                <a href="assets/list.html">view</a>
                                                <div class="v-separator"></div>
                                                <a href="public/assets/list.html" download="public/assets/list.html">download</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="motion-slide-in-top dbl-margin-bottom">
                                        <div class="row">
                                            <div class="col-6">
                                                <a href="assets/sidebar.html">
                                                    <img class="thumb" src="public/img/sidebar-example-thumb.png">
                                                </a>
                                            </div>
                                            <div class="col-6">
                                                <div class="subtitle">Sidebar</div>
                                                <p>Sample Sales Portal application with sidebar.</p>
                                                <a href="assets/sidebar.html">view</a>
                                                <div class="v-separator"></div>
                                                <a href="public/assets/sidebar.html" download="public/assets/sidebar.html">download</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="tabshome-releases-content" class="tab-pane">
                        <h1>Previous Releases</h1>
                        <div class="section">
                            <div class="row">
                                <div class="col-12">
                                    <table class="table table--lined">
                                        <thead>
                                            <th>Version</th>
                                            <th>Released</th>
                                            <th>&nbsp;</th>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td colspan="3">
                                                    <div class="panel no-padding">
                                                        <span class="text-bold">2019</span>
                                                    </div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>2.0.0</td>
                                                <td>August 21</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/2.0.0-official/" class="base-margin-right">docs</a>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/2.0.0-official/section-changelog.html">change log</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.3.5</td>
                                                <td>March 20</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.3.5-official/" class="base-margin-right">docs</a>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.3.5-official/section-changelog.html">change log</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.3.4</td>
                                                <td>January 2</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.3.4-official/" class="base-margin-right">docs</a>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.3.4-official/section-changelog.html">change log</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="3">
                                                    <div class="panel no-padding">
                                                        <span class="text-bold">2018</span>
                                                    </div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.3.3</td>
                                                <td>December 3</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.3.3-official/" class="base-margin-right">docs</a>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.3.3-official/section-changelog.html">change log</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.3.2</td>
                                                <td>October 15</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.3.2-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.3.0</td>
                                                <td>June 2</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.3.0-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.2.3</td>
                                                <td>February 12</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.2.2-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="3">
                                                    <div class="panel no-padding">
                                                        <span class="text-bold">2017</span>
                                                    </div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.2.0</td>
                                                <td>December 15</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.2.0-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.1.0</td>
                                                <td>October 4</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.1.0-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.0.5</td>
                                                <td>August 3</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.0.5-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="3">
                                                    <div class="panel no-padding">
                                                        <span class="text-bold">2016</span>
                                                    </div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.0.3</td>
                                                <td>December 13</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.0.3-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.0.2</td>
                                                <td>November 1</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.0.2-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.0.1</td>
                                                <td>September 1</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.0.1-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>1.0.0</td>
                                                <td>July 9</td>
                                                <td>
                                                    <a target="_blank" href="http://swtg-rtp-dev-7/styleguide-dist/1.0.0-official/" class="base-margin-right">docs</a>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="tabshome-migration-content" class="tab-pane migration">
                        <div class="flex-center-vertical">
                            <h1 class="flex-panel">Migration Guide</h1>
                            <h1 class="flex-panel flex-right">1.3.5 &#8594; 2.0.x</h1>
                        </div>
                        <div class="section">
                            <div class="subheader">Global</div>
                            <ul>
                                <li>
                                    <span>Make sure you add the UTF-8 encoding meta tag inside the head section of your main application file. Without this, the icons will not render properly.</span>
                                    <pre>
                                        <code>&lt;meta charset="utf-8"&gt;</code>
                                    </pre>
                                </li>
                                <li>Default page bed width is now <b>1600px</b>. However, the kit does support a max width of <b>2560px</b>. Use the container class `container-fluid` to widen the page bed out to 2560px.</li>
                                <li>The global modifiers are no longer supported. Animations and header margins are enabled by default.</li>
                                <li>We have moved to the new theme color palette. This means we now use a standard naming convention (e.g. primary, secondary, tertiary, success, ...).</li>
                                <li>Change all occurrences of <code>vibblue</code> to <code>primary</code>.</li>
                                <li>Change all occurrences of <code>blue</code> to <code>secondary</code>.</li>
                                <li>Change all occurrences of <code>indigo</code> to <code>tertiary</code>.</li>
                                <li>Remove all occurrences of <code>ltgray</code>, <code>mdgray</code>, and <code>ltblue</code>. Use the default version of that pattern instead.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader"><a href="section-primitives.html#primitives-button">Buttons</a></div>
                            <ul>
                                <li>Default button height was reduced from 40px to 30px. Use the modifier <code>btn--large</code> to use the 40px button.</li>
                                <li>Negative, Gray Ghost, White, and White Ghost buttons are no more. The new <code>btn--ghost</code> button replaces the Gray Ghost and White Ghost buttons. Look at using the <code>btn--link</code> instead of the old white button.</li>
                                <li>Button icons are now called Circle buttons and use the modifier <code>btn--circle</code> instead of <code>btn--icon</code>. The old modifier class still works but is deprecated.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader">Card</div>
                            <ul>
                                <li>Card pattern has been removed. Use Panel instead.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader">Carousel</div>
                            <ul>
                                <li>Carousel pattern has been removed. Use combination of circle buttons and icons instead.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader">Divider</div>
                            <ul>
                                <li>Divider pattern has been removed. Use horizontal rule instead.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader">Figure</div>
                            <ul>
                                <li>Figure is still supported but is no longer considered a first class pattern with its own separate docs page.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader"><a href="section-layout.html#layout-footer">Footer</a></div>
                            <ul>
                                <li>Default footer pattern no longer supported. Use the new simplified legal footer instead.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader"><a href="section-layout.html#layout-header">Header</a></div>
                            <ul>
                                <li>Header has undergone the most change in this release. The new header has been greatly simplified allowing for more flexibility of the content.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader">Hero</div>
                            <ul>
                                <li>Hero has been removed. Use Panel instead.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader"><a href="section-primitives.html#primitives-textfield">Input</a></div>
                            <ul>
                                <li>Input pattern has been renamed to Textfield.</li>
                                <li>Also textareas were moved out into their own docs page.</li>
                                <li>Floated labels are no more. Use stacked label (default) or inline labels instead.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader"><a href="section-primitives.html#primitives-label">Label</a></div>
                            <ul>
                                <li>Label colors now follow the theme color palette.</li>
                                <li>Tiny labels are no more. Use <code>label--small</code> instead.</li>
                                <li>Change <code>label--blue</code> to <code>label--secondary</code>.</li>
                                <li>Change <code>label--indigo</code> to <code>label--tertiary</code>.</li>
                                <li>Remove <code>label--lgray</code> or use default as it is no longer supported.</li>
                                <li>Remove <code>label--dkgray</code> as it is now the default color.</li>
                                <li>Remove <code>label--white</code> or use default as it is no longer supported.</li>
                                <li>Change <code>label--ghost</code> to use bordered label instead.</li>
                                <li>Change all <code>label--outlined</code> to <code>label--bordered</code>.</li>
                                <li>Circle labels are no more. Use circle button or badge instead.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader">List</div>
                            <ul>
                                <li>The modifiers <code>list--highlight</code>, <code>list--compressed</code>, and <code>list--loose</code> are no longer supported.</li>
                                <li>Lists are partially supported but are no longer considered a first class pattern with their own separate docs page.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader"><a href="section-primitives.html#primitives-panel">Panel</a></div>
                            <ul>
                                <li>Panel colors now follow the theme color palette.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader"><a href="section-primitives.html#primitives-switch">Switch</a></div>
                            <ul>
                                <li>Switch size reduced from 24px to 16px to match other similar form elements (radio, checkbox).</li>
                                <li>The modifier <code>switch--large</code> is no longer supported.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader">Thumbnail</div>
                            <ul>
                                <li>Thumbnail pattern has been removed. Use image helpers instead.</li>
                            </ul>
                        </div>
                        <hr>
                        <div class="base-margin-bottom">
                            <div class="subheader"><a href="section-components.html#components-timeline">Timeline</a></div>
                            <ul>
                                <li>Timeline pattern no longer supports colors. Instead use whatever icon and color you want in the timeline icon block.</li>
                            </ul>
                        </div>
                    </div>
                    <div id="tabshome-changelog-content" class="tab-pane">
                        <!-- inject:changelog -->
                        <!-- contents of html partials will be injected here -->
                        <!-- endinject -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

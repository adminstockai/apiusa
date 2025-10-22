$(document).ready(function () {
    var content = `
<div class="content-wrapper" data-afp-number="0">
<div class="user-page-section theme-class-01-exabytes pre-made">
<div class="container ">
    <div class="wrapper avatar-page-layout  one-col" id="userWrapper" data-visitor_country="KR" data-clickurl="" data-userid="7924652">
        <div class="user-page-section-content ">
            <div class="user-info-wrapper  user-one-col ">
                <div class="user-info ">
                    <img src="static/images/title.png" draggable="false" class="img-fluid" alt="" style="margin-bottom:20px;">
                    <div class="preview-user-description__component" style="padding:30px 20px; font-size: 1rem; line-height: 1.5;">
                        <div class="description-wrapper  center">
                            <p class="mb-0">
                                Enter your ticker symbol or stock symbol of interest below and the AI system
                                will analyze it in 1.5 seconds. Currently,
                                <strong id="counter" style="color:#90b1f6;">46,875</strong>  people are viewing the full report for free!
                                <br>
                                <strong style="color:#90b1f6;">96.8% prediction accuracy</strong>
                                <script>
                                    function parseNumber(str) {
                                        return parseInt(str.replace(/,/g, ''), 10);
                                    }
                                    function formatNumber(num) {
                                        return num.toLocaleString();
                                    }
                                    function updateCounter() {
                                        const el = document.getElementById('counter');
                                        let current = parseNumber(el.textContent);
                                        let increment = Math.floor(Math.random() * 10) + 1; // 1 到 10 之间
                                        current += increment;
                                        el.textContent = formatNumber(current);
                                    }
                                    // 每3秒更新一次
                                    setInterval(updateCounter, 2000);
                                </script>
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="blocks-wrapper">
                <div class="preview-links-list__component">

                    <div class="input-group mb-3">
                        <input type="text" class="form-control" placeholder="Please enter a valid stock symbol or keyword" aria-label="Stock symbol" style="height: 60px; font-size: 18px; padding: 10px 15px; border-radius: 8px;">
                    </div>
                    <div class="preview-link-item__component theme-class-01-exabytes  pop">
                        <a class="preview-link-wrapper d-flex justify-content-center align-items-center" href="javascript:void(0);" id="startAnalysisBtn">
                            <div>
                                <svg t="1753283144202" class="icon mr-2" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4612" width="38" height="38"><path d="M0 512c0 282.773333 229.226667 512 512 512s512-229.226667 512-512S794.773333 0 512 0 0 229.226667 0 512z" fill="#31B84C" p-id="4613"></path><path d="M192.021333 832l45.226667-164.330667a315.413333 315.413333 0 0 1-42.538667-158.528C194.730667 334.250667 337.706667 192 513.344 192c84.586667-0.213333 165.76 33.28 225.386667 93.013333A314.453333 314.453333 0 0 1 832 509.376c-0.085333 174.848-143.04 317.141333-318.656 317.141333h-0.149333c-53.205333 0-105.557333-13.290667-152.277334-38.613333L192 832h0.021333zM433.706667 376.533333c-6.442667-15.445333-13.013333-13.354667-17.92-13.610666-4.629333-0.213333-9.941333-0.256-15.253334-0.256a29.226667 29.226667 0 0 0-21.226666 9.898666c-7.296 7.957333-27.84 27.136-27.84 66.133334s28.501333 76.672 32.490666 81.962666c3.968 5.290667 56.149333 85.333333 136 119.637334 19.008 8.170667 33.813333 13.056 45.397334 16.704 19.072 6.037333 36.437333 5.184 50.133333 3.157333 15.296-2.282667 47.125333-19.2 53.76-37.674667 6.613333-18.56 6.613333-34.389333 4.650667-37.717333-1.984-3.264-7.296-5.269333-15.274667-9.237333-7.957333-3.946667-47.125333-23.125333-54.4-25.770667-7.296-2.666667-12.586667-3.968-17.92 3.946667-5.312 7.936-20.565333 25.792-25.194667 31.061333-4.650667 5.312-9.301333 5.973333-17.258666 2.005333-7.978667-3.968-33.621333-12.330667-64-39.338666-23.68-20.992-39.68-46.954667-44.330667-54.912-4.650667-7.914667-0.469333-12.202667 3.52-16.149334 3.562667-3.541333 7.936-9.258667 11.904-13.866666 3.989333-4.650667 5.333333-7.957333 7.978667-13.226667 2.645333-5.290667 1.322667-9.92-0.64-13.888-2.005333-3.968-17.92-42.986667-24.554667-58.858667h-0.021333z" fill="#FFFFFF" p-id="4614"></path></svg>
                            </div>
                            <div class="h5 mb-0 font-weight-bold">Start Analysis</div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</div>
</div>

<div class="ai-modal" id="ai-modal" style="display:none;position:fixed;top:219px;left:0;width:100vw;height:100vh;z-index:9999;background:rgba(0,0,0,0.7);">
<div class="ai-progress" id="ai-progress">
<div class="pro-box" style="background:#fff;border-radius:12px;padding:32px 18px;max-width:340px;margin:60px auto;">
    <div class="title" style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">

        <div class="word" style="font-size:20px;font-weight:bold;">Analysis in Progress...</div>
    </div>
    <div class="progress-box">
        <div class="item" style="margin-bottom:16px;">
            <div class="i-title" style="font-size:15px;">Market Analysis</div>
            <div class="layui-progress layui-progress-big" lay-filter="progress-1" style="background:#eee;border-radius:8px;height:16px;">
                <div class="layui-progress-bar" id="bar-1" lay-percent="0%" style="width: 0%;background:#90b1f6;height:100%;border-radius:8px;"></div>
            </div>
        </div>
        <div class="item" style="margin-bottom:16px;">
            <div class="i-title" style="font-size:15px;">Chart Analysis</div>
            <div class="layui-progress layui-progress-big" lay-filter="progress-2" style="background:#eee;border-radius:8px;height:16px;">
                <div class="layui-progress-bar" id="bar-2" lay-percent="0%" style="width: 0%;background:#90b1f6;height:100%;border-radius:8px;"></div>
            </div>
        </div>
        <div class="item">
            <div class="i-title" style="font-size:15px;">News Analysis</div>
            <div class="layui-progress layui-progress-big" lay-filter="progress-3" style="background:#eee;border-radius:8px;height:16px;">
                <div class="layui-progress-bar" id="bar-3" lay-percent="0%" style="width: 0%;background:#90b1f6;height:100%;border-radius:8px;"></div>
            </div>
        </div>
    </div>
</div>
</div>
<div class="ai-result" id="ai-result" style="display:none;">
<div class="result-box" style="background:#fff;border-radius:12px;padding:32px 18px;max-width:340px;margin:60px auto;">
    <div class="title" style="margin-bottom:18px;">
        <div class="word" style="font-size:18px;font-weight:bold;"><span id="tips-code" style="color:#15a223;"></span> Stock Analysis Report is Ready</div>
    </div>
    <div class="result-con">
        <div class="con" style="font-size:15px;margin-bottom:18px;">
            <div> To get a detailed stock report, please add the AI assistant. You will also receive today's
                3 recommended quality stocks.</div>
        </div>
        <div class="btn" id="chat-btn" style="background:#15a223;color:#fff;padding:12px 0;border-radius:8px;text-align:center;cursor:pointer;display:flex;justify-content:center;align-items:center;width:100%;margin:0 auto;animation:breath 1.6s infinite;" onclick="showline()">
            Receive Analysis Report for Free via WhatsApp
        </div>
    </div>
</div>
</div>
</div>

<div id="consent-banner" class="consent-banner">
<p style="margin-bottom: 10px; font-size: 14px;">We use cookies to improve your experience. By continuing to use our services,
you agree to our privacy policy.
</p>
<button id="accept-btn" style="border-radius: 5px; font-size: 14px;">Accept</button>
<button id="decline-btn" style="border-radius: 5px; font-size:14px;">Decline</button>
</div>
<footer style="position: fixed; bottom: 0; left: 0; width: 100%; background-color:#546ea4; padding: 10px 0; text-align: center; font-size: 12px; z-index: 100;">
<a href="disclaimer.html" style="color: #fff; text-decoration: none; margin: 0 10px;">Disclaimer</a>
<a href="terms.html#" style="color: #fff; text-decoration: none; margin: 0 10px;">Terms of Use</a>
<a href="privacy.html" style="color: #fff; text-decoration: none; margin: 0 10px;">Privacy Policy</a>
</footer>
`;
    $('body').html(content);
    document.getElementById("startAnalysisBtn").onclick = function () {
        var modal = document.getElementById("ai-modal");
        var progress = document.getElementById("ai-progress");
        var result = document.getElementById("ai-result");
        var bars = [
            document.getElementById("bar-1"),
            document.getElementById("bar-2"),
            document.getElementById("bar-3"),
        ];
        modal.style.display = "block";
        progress.style.display = "";
        result.style.display = "none";

        bars.forEach(function (bar) {
            bar.style.width = "0%";
            bar.setAttribute("lay-percent", "0%");
        });

        function animateBar(idx, cb) {
            let cur = 0;

            function step() {
                cur += Math.floor(Math.random() * 13) + 7;
                if (cur > 100) cur = 100;
                bars[idx].style.width = cur + "%";
                bars[idx].setAttribute("lay-percent", cur + "%");
                if (cur < 100) setTimeout(step, 30);
                else if (cb) cb();
            }

            step();
        }

        animateBar(0, function () {
            animateBar(1, function () {
                animateBar(2, function () {
                    progress.style.display = "none";
                    result.style.display = "";
                });
            });
        });
    };
    document.getElementById("chat-btn").onclick = function () {
        showline();
    };
});
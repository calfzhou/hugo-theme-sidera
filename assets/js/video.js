// Reader activation attaches the source; loading never calls play(). Each player
// owns its state/listeners so an unavailable file cannot disable another player.
(() => {
  for (const figure of document.querySelectorAll('[data-sidera-video]')) {
    const video = figure.querySelector('video');
    const button = figure.querySelector('.video-load');
    const status = figure.querySelector('.video-status');
    if (!video || !button || !status || !video.dataset.videoSrc) continue;
    button.hidden = false;
    button.addEventListener('click', () => {
      button.hidden = true;
      let timer;
      const update = state => {
        figure.dataset.state = state;
        status.textContent = status.dataset[state];
        if (state !== 'loading') clearTimeout(timer);
      };
      const fail = () => {
        update('error');
        // Do not leave keyboard focus on a now-hidden loading control.
        if (document.activeElement === video || document.activeElement === button) {
          figure.querySelector('.video-source').focus();
        }
        video.hidden = true;
      };
      video.addEventListener('loadeddata', () => {
        video.hidden = false;
        update('ready');
      }, { once: true });
      video.addEventListener('error', fail);
      update('loading');
      // A stalled request has a visible bounded failure state, not an endless
      // spinner/retry. If the browser later succeeds, loadeddata restores controls.
      timer = setTimeout(fail, 15000);
      try {
        video.hidden = false;
        video.preload = 'auto';
        video.src = video.dataset.videoSrc;
        video.load();
        video.focus();
      } catch { fail(); }
    }, { once: true });
  }
})();

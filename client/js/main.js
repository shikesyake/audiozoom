window.AudioContext = window.AudioContext || window.webkitAudioContext;

// --- メディアソース選択 ---
const mediaSelect = document.getElementById('media_select');

if (mediaSelect) {
  mediaSelect.addEventListener('change', function() {
    const selectedPath = this.value;
    const selectedType = this.options[this.selectedIndex]?.dataset.type;
    
    if (!selectedPath) {
      console.log('メディアが選択されていません');
      return;
    }
    
    console.log('選択されたメディア:', selectedPath, 'タイプ:', selectedType);
    
    if (selectedType === 'hls') {
      // HLS形式
      const fullPath = '/' + selectedPath;
      player.src({
        src: fullPath,
        type: 'application/x-mpegURL'
      });
      if (document.getElementById('play_btn').style.display !== 'none') {
        player.play();
      }
    } else if (selectedType === 'video') {
      // 動画ファイル（mp4など）
      const fullPath = '/' + selectedPath;
      player.src({
        src: fullPath,
        type: 'video/mp4'
      });
      if (document.getElementById('play_btn').style.display !== 'none') {
        player.play();
      }
    } else if (selectedType === 'audio') {
      // 音声
      const fullPath = '/' + selectedPath;
      audio1.src = fullPath;
      audio1.play();
    }
  });
}

//出力先
const output = document.querySelector('#output');

//マウス移動時
document.onmousemove = onmousemove;
onmousemove = function(e) {
  output1.innerHTML = `x:` + e.pageX + ` y:` + (e.pageY - 250);
  if (e.pageX < 200);
}

const audio = new AudioContext(); // 音声ファイルを指定

// Video.jsプレーヤーの初期化
const player = videojs('video', {
  controls: true,
  autoplay: false,
  preload: 'auto',
  width: 1280,
  height: 720,
  html5: {
    hls: {
      overrideNative: true
    }
  }
});

const video = player.el().querySelector('video');
const audio1 = document.getElementById('audio1');
const audio2 = document.getElementById('audio2');

// const track3 = audio.createMediaElementSource(videoElement);
const track1 = audio.createMediaElementSource(audio1);
const track2 = audio.createMediaElementSource(audio2);

const gainNode1 = audio.createGain();
const gainNode2 = audio.createGain();

track1.connect(gainNode1).connect(audio.destination);
track2.connect(gainNode2).connect(audio.destination);

audio.loop = true; // ループ再生を有効化

const vidurl = '../../live/video/video.m3u8';
const audiourl1 = '../../live/audio1/audio.m3u8';
const audiourl2 = '../../live/audio2/audio.m3u8';

// Video.jsでHLS対応
player.src({
  src: vidurl,
  type: 'application/x-mpegURL'
});

if (Hls.isSupported()) {
	const audiohls1 = new Hls();
	audiohls1.loadSource(audiourl1);
	audiohls1.attachMedia(audio1);
	
	const audiohls2 = new Hls();
	audiohls2.loadSource(audiourl2);
	audiohls2.attachMedia(audio2);
} else if (audio1.canPlayType('application/vnd.apple.mpegurl')) {
	audio1.src = audiourl1;
	audio2.src = audiourl2;
}

document.getElementById('play_btn')
  .addEventListener('click', function() {
    const btn = this;
    audio.resume().then(() => {
      btn.style.display = 'none';
      player.currentTime(1.17);
      player.volume(0);
      player.play();
      
      audio1.play();
      audio2.play();
    });
  }, false);

  

// --- 動画ズーム機能 ---
// const video = document.querySelector('.video');
const videoWrapper = document.querySelector('.video-wrapper');
const videoElement = document.querySelector('#video'); // Video.js要素
let scale = 1;

videoElement.addEventListener('wheel', function(e) {
  e.preventDefault();

  // videoWrapper内でのマウス座標を取得
  const rect = videoElement.getBoundingClientRect();
  const wrapperRect = videoWrapper.getBoundingClientRect();
  const offsetX = e.clientX - rect.left;
  const offsetY = e.clientY - rect.top;
  const percentX = (offsetX / rect.width) * 100;
  const percentY = (offsetY / rect.height) * 100;

  // transform-originをマウス位置に
  videoElement.style.transformOrigin = `${percentX}% ${percentY}%`;

  // ホイール上で拡大、下で縮小
  if (e.deltaY < 0) {
    scale += 0.1;
  } else {
    scale -= 0.1;
  }
  // 最小・最大倍率を制限（最小1に変更）
  scale = Math.max(1, Math.min(scale, 5));
  videoElement.style.transform = `scale(${scale})`;
});

let isDragging = false;
let dragStart = { x: 0, y: 0 };
let origin = { x: 50, y: 50 }; // デフォルトは中央

videoWrapper.addEventListener('mousedown', function(e) {
  isDragging = true;
  dragStart.x = e.clientX;
  dragStart.y = e.clientY;
  // ドラッグ開始時のoriginを記録
  origin.x = parseFloat(videoElement.style.transformOrigin.split('%')[0]) || 50;
  origin.y = parseFloat(videoElement.style.transformOrigin.split('%')[1]) || 50;
});

document.addEventListener('mouseup', function(e) {
  isDragging = false;
});

videoWrapper.addEventListener('mousemove', function(e) {
  if(scale === 1) return; // 拡大していないときは移動しない
  if (!isDragging) return;
  const offsetX = e.clientX;
  const offsetY = e.clientY;
  // ドラッグ量を計算
  // console.log(videoWrapper.clientWidth);
  const dx = ((offsetX - dragStart.x) / videoWrapper.clientWidth) * 100 / (scale-1);
  const dy = ((offsetY - dragStart.y) / videoWrapper.clientHeight) * 100 / (scale-1);
  // originを移動
  let newX = origin.x - dx;
  let newY = origin.y - dy;
  // 0～100%に制限
  newX = Math.max(0, Math.min(newX, 100));
  newY = Math.max(0, Math.min(newY, 100));
  videoElement.style.transformOrigin = `${newX}% ${newY}%`;

  // 中心座標（ズーム・パン後のvideoの中心がvideoWrapper内でどこか）
  // transform-origin（%）→ px
  const centerOriginX = newX / 100 * videoWrapper.clientWidth;
  const centerOriginY = newY / 100 * videoWrapper.clientHeight;
  // ズーム倍率を考慮して中心座標を計算
  const Xc = centerOriginX + (videoWrapper.clientWidth / 2 - centerOriginX) / scale;
  const Yc = centerOriginY + (videoWrapper.clientHeight / 2 - centerOriginY) / scale;

  for (const data of audiodata) {
    // console.log(data.tag, data.x, data.y, Math.hypot(Xc - data.x, Yc - data.y));
    const distance = Math.hypot(Xc - data.x, Yc - data.y);
    // console.log(data.tag, data.x, data.y, distance);
    let v = distance / maxDist;
    v = Math.max(0, Math.min(v, 1)); // 0～1にクリップ
    console.log(v);
    data.tag.gain.value = Math.pow(1 - v, scale);

    console.log('gain:', data.tag.gain.value);
  }
  setCenter(Xc, Yc);
  output.innerHTML = `中心座標: x:${Xc.toFixed(1)}px y:${Yc.toFixed(1)}px | origin: x:${newX.toFixed(1)}% y:${newY.toFixed(1)}%`;
});

// 最大距離
const maxDist = 800;
const audiodata = [
  {x:200, y:600, tag:gainNode1},
  {x:1080, y:120, tag:gainNode2},
];

let Xcenter = window.innerWidth / 2;
let Ycenter = window.innerHeight / 2;

// 動画の中心座標を更新する関数
function setCenter(x, y) {
  Xcenter = x;
  Ycenter = y;
}


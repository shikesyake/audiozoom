window.AudioContext = window.AudioContext || window.webkitAudioContext;

//出力先
const output = document.querySelector('#output');

//マウス移動時
document.onmousemove = onmousemove;
onmousemove = function(e) {
  output1.innerHTML = `x:` + e.pageX + ` y:` + (e.pageY - 250);
  if (e.pageX < 200);


}

// //マウス離脱時
// document.onmouseout = onmouseout;
// onmouseout = function(e) {
//   output.innerHTML = ``;
// }

const audio = new AudioContext(); // 音声ファイルを指定

const videoElement = document.querySelector('#video');
const audioElement = document.querySelector('#audio');
const audioElement2 = document.querySelector('#audio2');

// const track3 = audio.createMediaElementSource(videoElement);
const track = audio.createMediaElementSource(audioElement);
const track2 = audio.createMediaElementSource(audioElement2);

const gainNode = audio.createGain();
const gainNode2 = audio.createGain();

track.connect(gainNode).connect(audio.destination);
track2.connect(gainNode2).connect(audio.destination);

audio.loop = true; // ループ再生を有効化

document.getElementById('play_btn')
  .addEventListener('click', function() {
    audio.resume().then(() => {
      videoElement.currentTime = 1.17;
      videoElement.volume = 0.0;
      videoElement.play();
      
      audioElement.play();
      // audioElement.currentTime = 6;
      audioElement2.play();
      // audioElement2.currentTime = 5.86;

    });
  }, false);

  

let curX;
const WIDTH = window.innerWidth;

// マウスが動いたら新しいX座標を取得し、
// ゲインの値を設定する
document.onmousemove = updatePage;


// // マウスベースで音量を変える
// function updatePage(e) {
//   curX = e.pageX;
//   // gainNode.gain.value = curX / WIDTH;
//   // track.connect(gainNode).connect(audio.destination);

//   // audioのゲイン（X座標が右に行くほど音量が上がる）
//   const gainValue1 = curX / WIDTH;
//   // const gainValue1 = 0.3;
//   //console.log(gainNode.gain.value,gainNode.gain.maxValue,gainNode.gain.minValue)
//   gainNode.gain.value = gainValue1;
  
//   // audio2のゲイン（X座標が左に行くほど音量が上がる）
//   const gainValue2 = 1 - (curX / WIDTH);
//   // const gainValue2 = 0;
//   gainNode2.gain.value = gainValue2;
  
//   console.log(gainValue1,gainValue2);
//   track.connect(gainNode).connect(audio.destination);
//   track2.connect(gainNode2).connect(audio.destination);
// }

// origin基準で音量を変える
function updatePage(e) {
  // originXの位置でゲインを決定
  let originX = window.innerWidth / 2;
  let originY = window.innerHeight / 2;
  if (video && video.style.transformOrigin) {
    const [ox, oy] = video.style.transformOrigin.split(' ');
    if (ox.endsWith('%')) {
      originX = (parseFloat(ox) / 100) * window.innerWidth;
    } else if (ox.endsWith('px')) {
      originX = parseFloat(ox);
    }
    if (oy.endsWith('%')) {
      originY = (parseFloat(oy) / 100) * window.innerHeight;
    } else if (oy.endsWith('px')) {
      originY = parseFloat(oy);
    }
  }
}

  // 最大距離
const maxDist = 800;
const audiodata = [
  {x:200, y:600, tag:gainNode},
  {x:1080, y:120, tag:gainNode2},
  // {x:600, y:50, file:'audio/sample3.mp3'},
  // {x:900, y:50, file:'audio/sample4.mp3'},
  // {x:1200, y:50, file:'audio/sample5.mp3'},
];

let Xcenter = window.innerWidth / 2;
let Ycenter = window.innerHeight / 2;

// 動画の中心座標を更新する関数
function setCenter(x, y) {
  Xcenter = x;
  Ycenter = y;
  updatePage();
}

// --- 動画ズーム機能 ---
const video = document.querySelector('.video');
const videoWrapper = document.querySelector('.video-wrapper');
let scale = 1;

video.addEventListener('wheel', function(e) {
  e.preventDefault();

  // videoWrapper内でのマウス座標を取得
  const rect = video.getBoundingClientRect();
  const wrapperRect = videoWrapper.getBoundingClientRect();
  const offsetX = e.clientX - rect.left;
  const offsetY = e.clientY - rect.top;
  const percentX = (offsetX / rect.width) * 100;
  const percentY = (offsetY / rect.height) * 100;

  // transform-originをマウス位置に
  video.style.transformOrigin = `${percentX}% ${percentY}%`;

  // ホイール上で拡大、下で縮小
  if (e.deltaY < 0) {
    scale += 0.1;
  } else {
    scale -= 0.1;
  }
  // 最小・最大倍率を制限（最小1に変更）
  scale = Math.max(1, Math.min(scale, 5));
  video.style.transform = `scale(${scale})`;
});

let isDragging = false;
let dragStart = { x: 0, y: 0 };
let origin = { x: 50, y: 50 }; // デフォルトは中央

videoWrapper.addEventListener('mousedown', function(e) {
  isDragging = true;
  dragStart.x = e.clientX;
  dragStart.y = e.clientY;
  // ドラッグ開始時のoriginを記録
  origin.x = parseFloat(video.style.transformOrigin.split('%')[0]) || 50;
  origin.y = parseFloat(video.style.transformOrigin.split('%')[1]) || 50;
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
  video.style.transformOrigin = `${newX}% ${newY}%`;

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


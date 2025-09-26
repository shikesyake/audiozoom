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
const audioElement = document.querySelector('#audio');
const track = audio.createMediaElementSource(audioElement);

const audioElement2 = document.querySelector('#audio2');
const track2 = audio.createMediaElementSource(audioElement2);

audio.loop = true; // ループ再生を有効化

const gainNode = audio.createGain();
const gainNode2 = audio.createGain();

document.getElementById('play_btn')
  .addEventListener('click', function() {
    audio.resume().then(() => {
      audioElement.play();
      audioElement2.play();
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
  // マウスの位置は無視し、originXのみでゲインを決定
  let originX = window.innerWidth / 2; // デフォルト: 中央
  if (video && video.style.transformOrigin) {
    const [ox, ] = video.style.transformOrigin.split(' ');
    if (ox.endsWith('px')) {
      originX = parseFloat(ox);
    } else if (ox.endsWith('%')) {
      // %指定の場合はpxに変換
      originX = (parseFloat(ox) / 100) * window.innerWidth;
    }
  }

  // originXを0～window.innerWidthで正規化
  const relX = originX / window.innerWidth; // 0～1
  const gainValue1 = Math.max(0, Math.min(relX, 1));
  const gainValue2 = 1 - gainValue1;

  gainNode.gain.value = gainValue1;
  gainNode2.gain.value = gainValue2;

  track.connect(gainNode).connect(audio.destination);
  track2.connect(gainNode2).connect(audio.destination);
}

const audiodata = [
  {x:200, y:600, tag:'audioElement'},
  {x:1080, y:120, tag:'audioElement2'},
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
////////////////////////////////
// Todo ズームによる音量変化を追加
////////////////////////////////

// // 動画のtransform-originを基準に最も近いaudioを取得

// const targetValue = {x: Xcenter, y: Ycenter};
// // console.log(targetValue);

// // x, y両方の距離（ユークリッド距離）で最も近いaudioを取得
// const nearaudio = audiodata.reduce((prev, curr) => {
//   const prevDist = Math.hypot(prev.x - targetValue.x, prev.y - targetValue.y);
//   const currDist = Math.hypot(curr.x - targetValue.x, curr.y - targetValue.y);
//   return currDist < prevDist ? curr : prev;
// });

// 結果: audioElement または audioElement2

// // 三項演算子
// // ある条件 ? 条件がtrueのときの値 : 条件がfalseのときの値
// // 例:
// // ある条件
// const condition = (5 > 3);
// // 条件がtrueのときの値
// const exprIfTrue = '5は3より大きい';
// // 条件がfalseのときの値
// const exprIfFalse = '5は3より小さい';
// // 三項演算子で値を決定 (この場合はexprIfTrueが代入される)

// const kyori = condition ? exprIfTrue : exprIfFalse;




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
  setCenter(Xc, Yc);
  output.innerHTML = `中心座標: x:${Xc.toFixed(1)}px y:${Yc.toFixed(1)}px | origin: x:${newX.toFixed(1)}% y:${newY.toFixed(1)}%`;
});

// --- 音量制御 ---
function updatePage() {
  // 最大距離（例えば画面対角線長）で正規化
  const maxDist = Math.hypot(window.innerWidth, window.innerHeight);

  // 各音源との距離を計算し、近いほど音量が大きくなるように
  const dist1 = Math.hypot(Xcenter - audiodata[0].x, Ycenter - audiodata[0].y);
  const dist2 = Math.hypot(Xcenter - audiodata[1].x, Ycenter - audiodata[1].y);

  // 拡大率が上がるほど音量を下げる（例: 1/scale で減衰）
  const scaleAttenuation = 1 / scale;

  // 距離が0なら1、最大距離なら0
  let gainValue1 = (1 - (dist1 / maxDist)) * scaleAttenuation;
  let gainValue2 = (1 - (dist2 / maxDist)) * scaleAttenuation;

  // 0～1にクリップ
  gainValue1 = Math.max(0, Math.min(gainValue1, 1));
  gainValue2 = Math.max(0, Math.min(gainValue2, 1));

  gainNode.gain.value = gainValue1;
  gainNode2.gain.value = gainValue2;

  track.connect(gainNode).connect(audio.destination);
  track2.connect(gainNode2).connect(audio.destination);
}





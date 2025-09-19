window.AudioContext = window.AudioContext || window.webkitAudioContext;

//出力先
const output = document.querySelector('#output');

//マウス移動時
document.onmousemove = onmousemove;
onmousemove = function(e) {
  output.innerHTML = `x:` + e.pageX + ` y:` + e.pageY;
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

function updatePage(e) {
  curX = e.pageX;
  // gainNode.gain.value = curX / WIDTH;
  // track.connect(gainNode).connect(audio.destination);

  // audioのゲイン（X座標が右に行くほど音量が上がる）
  const gainValue1 = curX / WIDTH;
  // const gainValue1 = 0.3;
  //console.log(gainNode.gain.value,gainNode.gain.maxValue,gainNode.gain.minValue)
  gainNode.gain.value = gainValue1;
  
  // audio2のゲイン（X座標が左に行くほど音量が上がる）
  const gainValue2 = 1 - (curX / WIDTH);
  // const gainValue2 = 0;
  gainNode2.gain.value = gainValue2;
  
  track.connect(gainNode).connect(audio.destination);
  track2.connect(gainNode2).connect(audio.destination);
}


// // ウィンドウ全体でマウスの動きを監視
// window.addEventListener('mousemove', (event) => {
//   // マウスのX座標を取得
//   const mouseX = event.clientX;

//   // ウィンドウの幅を取得
//   const windowWidth = window.innerWidth;

//   // 音量を0～1の範囲にマッピング
//   const volume = Math.min(Math.max(mouseX / windowWidth, 0), 1);

//   // 音量を設定
//   audio.volume = volume;

//   console.log(`Volume: ${volume}`); // デバッグ用に音量を表示
// });
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
  console.log(videoWrapper.clientWidth);
  const dx = ((offsetX - dragStart.x) / videoWrapper.clientWidth) * 100 / (scale-1);
  const dy = ((offsetY - dragStart.y) / videoWrapper.clientHeight) * 100 / (scale-1);
  // originを移動
  let newX = origin.x - dx;
  let newY = origin.y - dy;
  // 0～100%に制限
  newX = Math.max(0, Math.min(newX, 100));
  newY = Math.max(0, Math.min(newY, 100));
  video.style.transformOrigin = `${newX}% ${newY}%`;
  console.log(newX,newY);
});





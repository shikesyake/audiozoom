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
const audioElement = document.querySelector('audio');
const track = audio.createMediaElementSource(audioElement);

audio.loop = true; // ループ再生を有効化

document.getElementById('play_btn')
  .addEventListener('click', function() {
    track.connect(gainNode);
    audioElement.play();
  }, false);

  
const gainNode = audio.createGain();

let curX;
const WIDTH = window.innerWidth;

// マウスが動いたら新しいY座標を取得し、
// ゲインの値を設定する
document.onmousemove = updatePage;

function updatePage(e) {
  curX = e.pageX;
  gainNode.gain.value = curX / WIDTH;
  track.connect(gainNode).connect(audio.destination);
}

const audio2 = new AudioContext(); // 音声ファイルを指定
const audioElement2 = document.querySelector('audio2');
const track2 = audio.createMediaElementSource(audioElement2);

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






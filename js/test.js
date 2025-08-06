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
  gainNode.gain.value = gainValue1;
  
  // audio2のゲイン（X座標が左に行くほど音量が上がる）
  const gainValue2 = 1 - (curX / WIDTH);
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






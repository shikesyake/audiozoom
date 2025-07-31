// let ball = {};
// // const soundFile;

// function preload() {
//     soundFormats('mp3', 'ogg','wav');
//     soundFile = loadSound('Mrs_Robinson.mp3');
// }

// function setup() {
//     createCanvas(710, 100);
// }

// function draw() {
//     background(0);
//     ball.x = constrain(mouseX, 0, width);
//     ellipse(ball.x, height / 2, 100, 100);
// }

// function mousePressed() {
//     // ボールのx位置を、-1(左)と1(右)の間のパンの度合いにマッピングする
//     let panning = map(ball.x, 0, width, -1.0, 1.0);
//     soundFile.pan(panning);
//     soundFile.play();
// }


// p5.SoundFileオブジェクト
let song;

function preload() {
    // サウンドファイルの読み込み
    song = loadSound('js/Mrs_Robinson.mp3');
}

function setup() {
    createCanvas(710, 600);

    // Chromeの自動再生ポリシーに沿うため、ここでsong.loop()は実行しない

    // 代わりにボタンのクリックでループ再生と停止を切り替える
    const button = setButton('LOOP', {
        x: 600,
        y: 10
    });
    button.mousePressed(() => {
        if (song.isPlaying()) {
            song.stop();
            button.html('LOOP');
        }
        else {
            // ループ再生
            song.play();
            button.html('STOP');
        }
    });
}

function draw() {
    background(200);

    // 音量を0と1の範囲におさめる
    let volume = map(mouseX, 250, 0, 0, 1);
    volume = constrain(volume, 0, 1);
    song.amp(volume);

    // レートを0.01と4の範囲におさめる
    // レートの変更によってピッチが変わる
    // let speed = map(mouseY, 0.1, height, 0, 2);
    // speed = constrain(speed, 0.01, 4);
    // song.rate(speed);

    // mouseXとmouseYの変化を円の位置で示す
    stroke(0);
    fill(51, 100);
    ellipse(mouseX, 100, 48, 48);
    stroke(0);
    fill(51, 100);
    ellipse(100, mouseY, 48, 48);
}

function setButton(label, pos) {
    const button = createButton(label);
    button.size(100, 30);
    button.position(pos.x, pos.y);
    return button;
}
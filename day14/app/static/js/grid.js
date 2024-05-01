//const container = document.getElementById("container");
// document.querySelector("#ffwd").addEventListener("click", startSimulation)
const COL_SAND = (255, 204, 0);
const COL_ROCK = (150,150 ,150);
let COL_SOURCE = (255, 45, 0);
let data;
let grid;
let cols, rows;
let w = 10;
let counter = 0;

function make2DArray(cols, rows) {
  let arr = new Array(cols);
  for (let i = 0; i < arr.length; i++) {
    arr[i] = new Array(rows);
    // Fill the array with 0s
    for (let j = 0; j < arr[i].length; j++) {
      arr[i][j] = 0;
    }
  }
  return arr;
}

function insertDataIn2DArray(data) {
  h_data = data.length;
  w_data = data[0].length;
  h_grid = grid.length;
  w_grid = grid[0].length;
  x_shft = Math.floor((w_grid - w_data) / 2);
  y_shft = w_grid - w_data - 1;
  for (i=0; i<data.length; i++) {
    for (j=0; j<data[i].length; j++){
      grid[j+y_shft][i+x_shft] = data[j][i];
    }
  }
}

function setup() {
  createCanvas(800, 800);
  frameRate(10);
  cols = width / w;
  rows = height / w;
  grid = make2DArray(cols, rows);
  httpGet("api/regolithInitial", "json", false, response => insertDataIn2DArray(response) );

}

function draw() {
  background(0);
  textSize(30);
  text(counter, 40, 40);
  counter = 0;
  for (let i = 0; i < cols; i++) {
    for (let j = 0; j < rows; j++) {
      noStroke();
      if (grid[j][i] !== 0) {
        switch (grid[j][i]) {
          case 1:
            fill(COL_ROCK);
            break;
          case 2:
            fill('red');
            break;
          case 3:
            fill('orange');
            break;
        }
        let x = i * w;
        let y = j * w;
        square(x, y, w);
      }
    }
  }
  let nextGrid = make2DArray(cols, rows)
  for (i=1; i<cols-1; i++) {
    for (j=1; j<rows; j++) {
      let state = grid[i][j];
      if (state === 3) {
        let belowCenter = grid[i+1][j];
        let belowLeft = grid[i+1][j-1];
        let belowRight = grid[i+1][j+1];
        if (belowCenter === 0) {
          nextGrid[i+1][j] = state;
        } else if(belowLeft === 0) {
          nextGrid[i+1][j-1] = state;
        } else if (belowRight === 0) {
          nextGrid[i+1][j+1] = state;
        } else {
          nextGrid[i][j] = state;
          counter += 1;
        }
      }
      if (state === 2) {
        nextGrid[i][j] = 2;
        if ((frameCount%3) === 0) {
          nextGrid[i+1][j] = 3;
        }
      }
      if (state === 1) {
        nextGrid[i][j] = state;
      }
    }
  }
  grid = nextGrid;
}

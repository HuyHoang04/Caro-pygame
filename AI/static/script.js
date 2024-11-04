const boardElement = document.getElementById("board");
const statusElement = document.getElementById("status");

function createBoard(board) {
  boardElement.innerHTML = "";
  board.forEach((row, rowIndex) => {
    row.forEach((cell, colIndex) => {
      const cellElement = document.createElement("div");
      cellElement.classList.add("cell");
      cellElement.textContent = cell;
      cellElement.addEventListener("click", () =>
        playerMove(rowIndex, colIndex)
      );
      boardElement.appendChild(cellElement);
    });
  });
}

async function playerMove(row, col) {
  const response = await fetch("/move", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ row, col }),
  });
  const data = await response.json();
  createBoard(data.board);
  if (data.winner) {
    statusElement.textContent = `${data.winner} thắng!`;
    boardElement.innerHTML = "";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  createBoard(Array.from({ length: 15 }, () => Array(15).fill("")));
});

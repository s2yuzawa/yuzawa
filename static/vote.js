// Ajaxリクエストを使って投票結果を取得し、表示する
function updateVoteResults() {
    fetch('/get-vote-results')  // Flaskエンドポイント
        .then(response => response.json())
        .then(data => {
            const resultsElement = document.getElementById('vote-results');
            resultsElement.innerHTML = '';  // 既存の内容をクリア
            data.forEach(result => {
                const resultDiv = document.createElement('div');
                resultDiv.textContent = `${result.playerName}: ${result.votes} votes`;
                resultsElement.appendChild(resultDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}

// ページ読み込み後に投票結果を更新
document.addEventListener('DOMContentLoaded', function() {
    updateVoteResults();
});

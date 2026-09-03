const uploadBtn = document.getElementById('upload-btn');
const statusText = document.getElementById('status-text');

uploadBtn.addEventListener('click', async () => {
    const filePath = await window.electronAPI.openFile();
    if (filePath) {
        statusText.innerText = `Selected: ${filePath}`;
        // Here we would use axios/fetch to post to our local FastAPI backend
        // e.g. POST http://localhost:8000/upload
    }
});

// Mock Plotly initialization
const plotDiv = document.getElementById('waveform-plot');
const trace1 = { x: [1, 2, 3, 4], y: [10, 15, 13, 17], type: 'scatter', name: 'Z' };
const trace2 = { x: [1, 2, 3, 4], y: [16, 5, 11, 9], type: 'scatter', name: 'N' };
const layout = {
    paper_bgcolor: '#1e1e1e',
    plot_bgcolor: '#1e1e1e',
    font: { color: '#e0e0e0' },
    margin: { t: 20, l: 30, r: 10, b: 30 }
};
Plotly.newPlot(plotDiv, [trace1, trace2], layout);

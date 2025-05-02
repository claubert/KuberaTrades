document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('candlestickFundo').getContext('2d');
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;

    const dados = [];
    const inicio = new Date();
    for (let i = 0; i < 50; i++) {
        const aberto = Math.random() * 100 + 100;
        const fechado = aberto + (Math.random() * 20 - 10);
        const alto = Math.max(aberto, fechado) + Math.random() * 5;
        const baixo = Math.min(aberto, fechado) - Math.random() * 5;
        dados.push({
            x: new Date(inicio.getTime() + i * 3600000),
            o: aberto,
            h: alto,
            l: baixo,
            c: fechado
        });
    }

    new Chart(ctx, {
        type: 'candlestick',
        data: {
            datasets: [{
                label: 'Candlestick',
                data: dados
            }]
        },
        options: {
            animation: {
                duration: 2000,
                easing: 'linear',
                loop: true
            },
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { type: 'time', time: { unit: 'hour' } },
                y: { beginAtZero: false }
            }
        }
    });
});
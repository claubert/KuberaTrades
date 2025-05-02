document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('candlestickFundo').getContext('2d');
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;

    let dados = [];
    const inicio = new Date();

    // Gerar dados iniciais
    function gerarDados() {
        dados = [];
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
    }

    gerarDados();

    const grafico = new Chart(ctx, {
        type: 'candlestick',
        data: {
            datasets: [{
                label: 'Mercado Financeiro',
                data: dados,
                borderColor: '#00ff00',
                color: {
                    up: '#00ff00',
                    down: '#ff0000'
                }
            }]
        },
        options: {
            animation: {
                duration: 1000,
                easing: 'easeInOutQuad'
            },
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { type: 'time', time: { unit: 'hour' }, display: false },
                y: { beginAtZero: false, display: false }
            }
        }
    });

    // Atualizar dados a cada 5 segundos
    setInterval(() => {
        const ultimo = dados[dados.length - 1];
        const novoAberto = ultimo.c;
        const novoFechado = novoAberto + (Math.random() * 20 - 10);
        const novoAlto = Math.max(novoAberto, novoFechado) + Math.random() * 5;
        const novoBaixo = Math.min(novoAberto, novoFechado) - Math.random() * 5;
        dados.shift();
        dados.push({
            x: new Date(ultimo.x.getTime() + 3600000),
            o: novoAberto,
            h: novoAlto,
            l: novoBaixo,
            c: novoFechado
        });
        grafico.update();
    }, 5000);
});
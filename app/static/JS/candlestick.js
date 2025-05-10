document.addEventListener('DOMContentLoaded', () => {
    console.log("Script candlestick.js carregado.");

    // Verificar se Chart.js e o plugin estão disponíveis
    if (!window.Chart || !Chart.controllers.financial) {
        console.error("Chart.js ou chartjs-chart-financial não está carregado corretamente.");
        return;
    }
    console.log("Chart.js e plugin financeiro carregados com sucesso.");

    // Criar canvas para fundo
    const canvas = document.createElement('canvas');
    canvas.id = 'marketBackground';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0.3'; // Fundo semi-transparente
    document.body.insertBefore(canvas, document.body.firstChild); // Inserir no início do body
    console.log("Canvas criado e adicionado ao body.");

    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error("Não foi possível obter o contexto 2D do canvas.");
        return;
    }
    console.log("Contexto 2D obtido com sucesso.");

    // Definir tamanho inicial do canvas
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    console.log(`Tamanho do canvas: ${canvas.width}x${canvas.height}`);

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
    console.log("Dados iniciais gerados:", dados);

    // Configurar gráfico como fundo
    try {
        const grafico = new Chart(ctx, {
            type: 'candlestick',
            data: {
                datasets: [{
                    label: 'Mercado Financeiro',
                    data: dados,
                    borderColor: 'rgba(0, 255, 0, 0.5)',
                    backgroundColor: 'rgba(0, 255, 0, 0.2)',
                    color: {
                        up: 'rgba(0, 255, 0, 0.5)',
                        down: 'rgba(255, 0, 0, 0.5)'
                    }
                }]
            },
            options: {
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuad'
                },
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: { unit: 'hour' },
                        display: false
                    },
                    y: {
                        beginAtZero: false,
                        display: false
                    }
                }
            }
        });
        console.log("Gráfico candlestick inicializado com sucesso.");

        // Atualizar dados a cada 5 segundos
        setInterval(() => {
            console.log("Atualizando dados do gráfico...");
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

        // Ajustar tamanho do canvas ao redimensionar a janela
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            grafico.resize();
            console.log(`Canvas redimensionado para: ${canvas.width}x${canvas.height}`);
        });
    } catch (error) {
        console.error("Erro ao inicializar o gráfico candlestick:", error);
    }
});
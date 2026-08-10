document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Persistência do Modo Escuro ---
    const themeToggleBtn = document.getElementById('toggleTheme');
    const htmlElement = document.documentElement;

    const savedTheme = localStorage.getItem('theme') || 'light';
    htmlElement.setAttribute('data-bs-theme', savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            htmlElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // --- 2. REST + Fetch API + Filtro Dinâmico ---
    const taskList = document.getElementById('taskList');
    const filterStatus = document.getElementById('filterStatus');
    let allTasks = [];

    if (taskList) {
        fetchTasks();

        filterStatus.addEventListener('change', () => {
            renderTasks(filterStatus.value);
        });
    }

    function fetchTasks() {
        fetch('/api/tarefas')
            .then(res => res.json())
            .then(data => {
                allTasks = data;
                renderTasks('Todos');
            });
    }

    function renderTasks(filter) {
        taskList.innerHTML = '';

        const filtered = filter === 'Todos' ? allTasks : allTasks.filter(t => t.status === filter);

        filtered.forEach(task => {
            // Mapeamento de cores conforme Desafio
            let bgClass = 'border-warning';
            let badgeClass = 'bg-warning text-dark';
            if (task.status === 'Em andamento') {
                bgClass = 'border-primary';
                badgeClass = 'bg-primary';
            } else if (task.status === 'Concluída') {
                bgClass = 'border-success';
                badgeClass = 'bg-success';
            }

            const card = document.createElement('div');
            card.className = 'col-md-4 mb-3';
            card.innerHTML = `
                <div class="card h-100 ${bgClass} border-2">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h5 class="card-title m-0">${task.titulo}</h5>
                            <span class="badge ${badgeClass}">${task.status}</span>
                        </div>
                        <p class="card-text">${task.descricao || ''}</p>
                    </div>
                    <div class="card-footer bg-transparent d-flex justify-content-end gap-2">
                        <a href="/editar/${task.id}" class="btn btn-sm btn-outline-secondary"><i class="bi bi-pencil"></i></a>
                        <button onclick="deleteTask(${task.id})" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></button>
                    </div>
                </div>
            `;
            taskList.appendChild(card);
        });
    }

    window.deleteTask = function(id) {
        if (confirm('Deseja excluir esta tarefa?')) {
            fetch(`/excluir/${id}`, { method: 'DELETE' })
                .then(res => res.json())
                .then(data => {
                    if (data.success) fetchTasks();
                });
        }
    };

    // --- 3. Dashboard com Chart.js ---
    const ctx = document.getElementById('statusChart');
    if (ctx) {
        fetch('/api/tarefas')
            .then(res => res.json())
            .then(data => {
                const counts = {
                    'Pendente': data.filter(t => t.status === 'Pendente').length,
                    'Em andamento': data.filter(t => t.status === 'Em andamento').length,
                    'Concluída': data.filter(t => t.status === 'Concluída').length,
                };

                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Pendente', 'Em andamento', 'Concluída'],
                        datasets: [{
                            data: [counts['Pendente'], counts['Em andamento'], counts['Concluída']],
                            backgroundColor: ['#ffc107', '#0d6efd', '#198754']
                        }]
                    }
                });
            });
    }
});
// Main JavaScript for Football Prediction Web App

const API_BASE = '/api';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('App initialized');
    loadDashboard();
    loadTeams();
    loadMatches();
    loadStatistics();
    setupPredictionForm();
});

// Load Dashboard Data
function loadDashboard() {
    fetch(`${API_BASE}/dashboard`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }
            
            document.getElementById('total-matches').textContent = data.total_matches;
            document.getElementById('total-teams').textContent = data.total_teams;
            document.getElementById('avg-goals').textContent = data.avg_goals;
            
            // Load chart data
            loadTeamChart();
            loadResultsChart();
        })
        .catch(error => console.error('Error loading dashboard:', error));
}

// Load Teams Data
function loadTeams() {
    fetch(`${API_BASE}/teams`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }
            
            // Populate teams table
            const teamsList = document.getElementById('teams-list');
            teamsList.innerHTML = '';
            
            data.teams.forEach((team, index) => {
                const row = `
                    <tr>
                        <td><strong>${index + 1}</strong></td>
                        <td>${team.team}</td>
                        <td>${team.matches}</td>
                        <td><span class="badge bg-success">${team.wins}</span></td>
                        <td><span class="badge bg-warning">${team.draws}</span></td>
                        <td><span class="badge bg-danger">${team.losses}</span></td>
                        <td>${team.goals_for}</td>
                        <td>${team.goals_against}</td>
                        <td>${team.goal_difference > 0 ? '+' : ''}${team.goal_difference}</td>
                        <td><strong>${team.points}</strong></td>
                        <td>
                            <button class="btn btn-sm btn-info" onclick="loadTeamDetail('${team.team}')">详情</button>
                        </td>
                    </tr>
                `;
                teamsList.innerHTML += row;
            });
            
            // Populate select dropdowns
            populateSelectOptions(data.teams);
        })
        .catch(error => console.error('Error loading teams:', error));
}

// Populate select options for prediction
function populateSelectOptions(teams) {
    const team1Select = document.getElementById('team1-select');
    const team2Select = document.getElementById('team2-select');
    
    teams.forEach(team => {
        const option1 = document.createElement('option');
        option1.value = team.team;
        option1.textContent = team.team;
        team1Select.appendChild(option1);
        
        const option2 = document.createElement('option');
        option2.value = team.team;
        option2.textContent = team.team;
        team2Select.appendChild(option2);
    });
}

// Load Team Detail
function loadTeamDetail(teamName) {
    fetch(`${API_BASE}/team/${encodeURIComponent(teamName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('球队未找到');
                return;
            }
            
            // Display team detail modal or panel
            const message = `
球队: ${data.team}
总场次: ${data.matches}
胜: ${data.wins} | 平: ${data.draws} | 负: ${data.losses}
进球: ${data.goals_for} | 失球: ${data.goals_against}
积分: ${data.points}
            `;
            alert(message);
        })
        .catch(error => console.error('Error loading team detail:', error));
}

// Load Matches
function loadMatches() {
    fetch(`${API_BASE}/matches`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }
            
            const matchesList = document.getElementById('matches-list');
            matchesList.innerHTML = '';
            
            data.matches.forEach(match => {
                const row = `
                    <tr>
                        <td>${match.date || '-'}</td>
                        <td>${match.home_team}</td>
                        <td><strong>${match.home_goals || '-'} - ${match.away_goals || '-'}</strong></td>
                        <td>${match.away_team}</td>
                        <td>
                            <span class="badge ${
                                match.result === 'Home Win' ? 'bg-success' :
                                match.result === 'Away Win' ? 'bg-danger' :
                                'bg-warning'
                            }">${match.result || '-'}</span>
                        </td>
                    </tr>
                `;
                matchesList.innerHTML += row;
            });
        })
        .catch(error => console.error('Error loading matches:', error));
}

// Load Statistics
function loadStatistics() {
    fetch(`${API_BASE}/statistics`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }
            
            document.getElementById('stat-home-wins').textContent = data.home_wins;
            document.getElementById('stat-draws').textContent = data.draws;
            document.getElementById('stat-away-wins').textContent = data.away_wins;
            document.getElementById('home-win-rate').textContent = 
                (data.home_win_rate * 100).toFixed(1) + '%';
        })
        .catch(error => console.error('Error loading statistics:', error));
}

// Load Team Chart
function loadTeamChart() {
    fetch(`${API_BASE}/teams`)
        .then(response => response.json())
        .then(data => {
            if (data.error || !data.teams.length) return;
            
            const teams = data.teams.slice(0, 10);
            const teamNames = teams.map(t => t.team);
            const points = teams.map(t => t.points);
            
            const trace = {
                x: teamNames,
                y: points,
                type: 'bar',
                marker: {
                    color: 'rgba(102, 126, 234, 0.8)',
                    line: {
                        color: 'rgba(102, 126, 234, 1)',
                        width: 1.5
                    }
                }
            };
            
            const layout = {
                title: '球队积分排行',
                xaxis: { title: '球队' },
                yaxis: { title: '积分' },
                margin: { b: 100 },
                paper_bgcolor: 'rgba(255,255,255,0)',
                plot_bgcolor: 'rgba(255,255,255,0)'
            };
            
            Plotly.newPlot('teams-chart', [trace], layout, { responsive: true });
        })
        .catch(error => console.error('Error loading team chart:', error));
}

// Load Results Chart
function loadResultsChart() {
    fetch(`${API_BASE}/statistics`)
        .then(response => response.json())
        .then(data => {
            if (data.error) return;
            
            const trace = {
                labels: ['主场胜', '平局', '客场胜'],
                values: [data.home_wins, data.draws, data.away_wins],
                type: 'pie',
                marker: {
                    colors: ['#28a745', '#ffc107', '#dc3545']
                }
            };
            
            const layout = {
                title: '比赛结果分布',
                paper_bgcolor: 'rgba(255,255,255,0)',
                plot_bgcolor: 'rgba(255,255,255,0)'
            };
            
            Plotly.newPlot('results-chart', [trace], layout, { responsive: true });
        })
        .catch(error => console.error('Error loading results chart:', error));
}

// Setup Prediction Form
function setupPredictionForm() {
    document.getElementById('prediction-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const team1 = document.getElementById('team1-select').value;
        const team2 = document.getElementById('team2-select').value;
        
        if (!team1 || !team2) {
            alert('请选择两支球队');
            return;
        }
        
        if (team1 === team2) {
            alert('请选择不同的球队');
            return;
        }
        
        predictMatch(team1, team2);
    });
}

// Predict Match
function predictMatch(team1, team2) {
    const formData = {
        team1: team1,
        team2: team2
    };
    
    fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('预测失败: ' + data.error);
            return;
        }
        
        displayPredictionResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('预测出错');
    });
}

// Display Prediction Results
function displayPredictionResults(data) {
    const resultsDiv = document.getElementById('prediction-results');
    const cardsDiv = document.getElementById('prediction-cards');
    
    const team1WinProb = (data.team1_win_prob * 100).toFixed(1);
    const drawProb = (data.draw_prob * 100).toFixed(1);
    const team2WinProb = (data.team2_win_prob * 100).toFixed(1);
    
    cardsDiv.innerHTML = `
        <div class="col-md-4">
            <div class="prediction-card win-prob">
                <h5>${data.team1} 赢</h5>
                <h2>${team1WinProb}%</h2>
            </div>
        </div>
        <div class="col-md-4">
            <div class="prediction-card draw-prob">
                <h5>平局</h5>
                <h2>${drawProb}%</h2>
            </div>
        </div>
        <div class="col-md-4">
            <div class="prediction-card loss-prob">
                <h5>${data.team2} 赢</h5>
                <h2>${team2WinProb}%</h2>
            </div>
        </div>
    `;
    
    document.getElementById('expected-goals-1').textContent = data.expected_goals.team1;
    document.getElementById('expected-goals-2').textContent = data.expected_goals.team2;
    
    resultsDiv.style.display = 'block';
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

console.log('Football Prediction App Loaded');

// Time & Weather Loop
setInterval(() => {
    const now = new Date();
    document.getElementById('time-text').innerText = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    document.getElementById('date-text').innerText = now.toLocaleDateString([], {weekday: 'long'}).toUpperCase();
}, 1000);

// Hardware Loop
eel.expose(update_hardware_stats);
function update_hardware_stats(stats) {
    // Bars
    document.getElementById('cpu-pct').innerText = Math.round(stats.cpu) + '%';
    document.getElementById('cpu-bar').style.width = stats.cpu + '%';
    document.getElementById('ram-pct').innerText = Math.round(stats.ram) + '%';
    document.getElementById('ram-bar').style.width = stats.ram + '%';
    document.getElementById('gpu-pct').innerText = Math.round(stats.gpu_load) + '%';
    document.getElementById('gpu-bar').style.width = stats.gpu_load + '%';

    // Sensors
    document.getElementById('batt-text').innerText = Math.round(stats.battery) + '%';
    document.getElementById('fan-text').innerText = stats.fan_speed + ' RPM';
    document.getElementById('gpu-temp-text').innerText = stats.gpu_temp + '°C';

    // Network
    if(stats.network) {
        document.getElementById('net-up').innerText = stats.network.up.toFixed(2);
        document.getElementById('net-down').innerText = stats.network.down.toFixed(2);
    }

    // Process Lists
    if(stats.top_procs) {
        const cpuList = document.getElementById('cpu-list');
        cpuList.innerHTML = stats.top_procs.cpu_apps.map(p => `<li><span>${p.name.substring(0, 18)}</span><span class="cyan">${p.val}%</span></li>`).join('');
        
        const ramList = document.getElementById('ram-list');
        ramList.innerHTML = stats.top_procs.mem_apps.map(p => `<li><span>${p.name.substring(0, 18)}</span><span class="orange">${p.val}%</span></li>`).join('');
    }

    // Audio / Privacy Apps
    const audioList = document.getElementById('audio-list');
    audioList.innerText = stats.audio_apps.length > 0 ? stats.audio_apps.join(', ') : 'None';

    const camList = document.getElementById('cam-list');
    const combinedCams = [...stats.camera_apps, ...stats.mic_apps];
    const uniqueCams = [...new Set(combinedCams)];
    camList.innerText = uniqueCams.length > 0 ? uniqueCams.join(', ') : 'None';
}

// Assistant State Loop
eel.expose(set_assistant_state);
function set_assistant_state(state, message) {
    const reactor = document.getElementById('arc-reactor');
    const statusText = document.getElementById('status-text');
    const subtitle = document.getElementById('subtitle-text');

    reactor.classList.remove('state-listening', 'state-speaking');

    if (state === 'LISTENING') {
        reactor.classList.add('state-listening');
        statusText.innerText = 'LISTENING...';
        statusText.className = 'status-text cyan';
    } else if (state === 'SPEAKING') {
        reactor.classList.add('state-speaking');
        statusText.innerText = 'SPEEDY ACTIVE';
        statusText.className = 'status-text orange';
    } else if (state === 'THINKING') {
        statusText.innerText = 'PROCESSING...';
        statusText.className = 'status-text cyan';
    } else {
        statusText.innerText = 'SYSTEM STANDBY';
        statusText.className = 'status-text cyan';
    }

    if (message) { subtitle.innerText = message; }
}

setInterval(() => {
    eel.get_system_stats()((stats) => {
        if(stats) update_hardware_stats(stats);
    });
}, 2000);

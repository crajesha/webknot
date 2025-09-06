# webknot<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Event Reporting Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Chosen Palette: Modern Slate Blue -->
    <!-- Application Structure Plan: The application is designed as a single-page dashboard with a top-level filter bar. This structure was chosen for its widespread familiarity and efficiency in data-driven applications. Users can immediately see the overall performance via KPI cards and then use the persistent filters at the top to drill down by college and event type. The user flow is straightforward: view the macro-level data, apply filters to narrow the scope, and then analyze the detailed charts and tables. This top-down approach is highly effective for administrative users who need to perform quick analysis and generate reports. -->
    <!-- Visualization & Content Choices: 
        - KPI Section: Inform -> Prominent Stat Cards -> Provides an immediate, high-level summary of the most critical metrics (events, registrations, attendance, feedback) -> HTML/JS.
        - Event Popularity Report: Compare -> Horizontal Bar Chart -> Effectively ranks events by registration numbers, directly fulfilling a core assignment requirement -> Chart.js.
        - Student Participation Report: Organize/Inform -> Interactive Table -> Lists students by their event attendance and highlights the top 3 performers, fulfilling a bonus requirement -> HTML/JS.
        - Registrations vs. Attendance: Compare -> Grouped Bar Chart -> Clearly visualizes the drop-off rate between registration and actual attendance, offering key insights for event planning -> Chart.js.
        - Feedback Score Distribution: Proportions -> Doughnut Chart -> Offers a quick, visual breakdown of student satisfaction through feedback ratings -> Chart.js.
        - Flexible Filtering: Interaction -> Top Filter Bar -> Enables users to dynamically filter all dashboard components by college and event type, satisfying a key bonus requirement for flexible reporting -> HTML/JS.
    -->
    <!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f1f5f9; /* Slate 100 */
        }
        .chart-container {
            position: relative;
            width: 100%;
            height: 350px;
            max-height: 400px;
        }
        .kpi-card {
            background-color: #ffffff;
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        }
        .table-container {
            max-height: 400px;
            overflow-y: auto;
        }
        .table-container thead th {
            position: sticky;
            top: 0;
            background-color: #f8fafc; /* Slate 50 */
        }
    </style>
</head>
<body class="text-gray-800">

    <div class="container mx-auto p-4 md:p-6 lg:p-8">
        
        <header class="mb-6">
            <h1 class="text-3xl md:text-4xl font-bold text-slate-800">Campus Event Dashboard</h1>
            <p class="text-slate-500 mt-2">Analyze event performance and student engagement across all colleges.</p>
        </header>

        <div class="bg-white rounded-xl shadow-sm p-4 mb-8 flex flex-col md:flex-row items-center justify-start gap-4 md:gap-6">
            <div class="w-full md:w-auto md:flex-1">
                <label for="collegeFilter" class="block text-sm font-medium text-slate-700 mb-1">College</label>
                <select id="collegeFilter" class="w-full p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
                    <option value="all">All Colleges</option>
                </select>
            </div>
            <div class="w-full md:w-auto md:flex-1">
                <label for="eventTypeFilter" class="block text-sm font-medium text-slate-700 mb-1">Event Type</label>
                <select id="eventTypeFilter" class="w-full p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
                    <option value="all">All Types</option>
                </select>
            </div>
        </div>

        <main>
            <section id="kpi-section" class="mb-8">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div class="kpi-card">
                        <h3 class="text-md font-semibold text-slate-500">Total Events</h3>
                        <p id="totalEvents" class="text-4xl font-bold text-blue-600 mt-2">0</p>
                    </div>
                    <div class="kpi-card">
                        <h3 class="text-md font-semibold text-slate-500">Total Registrations</h3>
                        <p id="totalRegistrations" class="text-4xl font-bold text-emerald-600 mt-2">0</p>
                    </div>
                    <div class="kpi-card">
                        <h3 class="text-md font-semibold text-slate-500">Avg. Attendance Rate</h3>
                        <p id="avgAttendance" class="text-4xl font-bold text-amber-500 mt-2">0%</p>
                    </div>
                    <div class="kpi-card">
                        <h3 class="text-md font-semibold text-slate-500">Avg. Feedback</h3>
                        <p id="avgFeedback" class="text-4xl font-bold text-violet-600 mt-2">0/5</p>
                    </div>
                </div>
            </section>
            
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                
                <div class="bg-white rounded-xl shadow-sm p-6">
                    <h2 class="text-xl font-bold mb-1 text-slate-800">Event Popularity Report</h2>
                    <p class="text-slate-600 mb-4 text-sm">Top 10 events ranked by number of registrations.</p>
                    <div class="chart-container">
                        <canvas id="popularityChart"></canvas>
                    </div>
                </div>

                <div class="bg-white rounded-xl shadow-sm p-6">
                    <h2 class="text-xl font-bold mb-1 text-slate-800">Student Participation Report</h2>
                    <p class="text-slate-600 mb-4 text-sm">Students ranked by events attended. Top 3 are highlighted.</p>
                    <div class="table-container">
                        <table class="w-full text-left">
                            <thead class="bg-slate-50 border-b-2 border-slate-200">
                                <tr>
                                    <th class="p-3 text-sm font-semibold tracking-wide">Rank</th>
                                    <th class="p-3 text-sm font-semibold tracking-wide">Student Name</th>
                                    <th class="p-3 text-sm font-semibold tracking-wide text-right">Events Attended</th>
                                </tr>
                            </thead>
                            <tbody id="studentTableBody"></tbody>
                        </table>
                    </div>
                </div>

                <div class="bg-white rounded-xl shadow-sm p-6">
                    <h2 class="text-xl font-bold mb-1 text-slate-800">Attendance vs. Registration</h2>
                    <p class="text-slate-600 mb-4 text-sm">Compares the registration vs. attendance for the top 10 most popular events.</p>
                    <div class="chart-container">
                        <canvas id="attendanceChart"></canvas>
                    </div>
                </div>

                <div class="bg-white rounded-xl shadow-sm p-6">
                    <h2 class="text-xl font-bold mb-1 text-slate-800">Feedback Score Distribution</h2>
                    <p class="text-slate-600 mb-4 text-sm">Breakdown of all feedback ratings (1-5) from event attendees.</p>
                     <div class="chart-container">
                        <canvas id="feedbackChart"></canvas>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        const mockData = { colleges: [], students: [], events: [], registrations: [], attendance: [], feedback: [] };
        const eventTypes = ["Workshop", "Fest", "Seminar", "Hackathon", "Tech Talk"];
        
        function generateMockData() {
            const numColleges = 50; const studentsPerCollege = 500; const eventsPerCollege = 20;
            let studentIdCounter = 1; let eventIdCounter = 1;

            for (let c = 1; c <= numColleges; c++) {
                mockData.colleges.push({ id: c, name: `College #${c}` });
                const collegeStudents = [];
                for (let s = 0; s < studentsPerCollege; s++) {
                    const student = { id: studentIdCounter, name: `Student ${studentIdCounter}`, college_id: c };
                    mockData.students.push(student); collegeStudents.push(student); studentIdCounter++;
                }
                for (let e = 0; e < eventsPerCollege; e++) {
                    const eventType = eventTypes[Math.floor(Math.random() * eventTypes.length)];
                    const event = { id: eventIdCounter, name: `${eventType} #${eventIdCounter}`, college_id: c, type: eventType };
                    mockData.events.push(event);
                    const numRegistrations = Math.floor(Math.random() * (studentsPerCollege * 0.2)) + 10;
                    const registeredStudents = [...collegeStudents].sort(() => 0.5 - Math.random()).slice(0, numRegistrations);
                    registeredStudents.forEach(student => {
                        mockData.registrations.push({ student_id: student.id, event_id: event.id });
                        if (Math.random() > 0.3) { 
                            mockData.attendance.push({ student_id: student.id, event_id: event.id });
                            if (Math.random() > 0.1) mockData.feedback.push({ student_id: student.id, event_id: event.id, rating: Math.floor(Math.random() * 3) + 3 });
                        }
                    });
                    eventIdCounter++;
                }
            }
        }

        let popularityChart, attendanceChart, feedbackChart;
        let filters = { college: 'all', type: 'all' };

        function init() {
            generateMockData();
            
            const collegeFilter = document.getElementById('collegeFilter');
            mockData.colleges.forEach(college => {
                const option = document.createElement('option');
                option.value = college.id; option.textContent = college.name;
                collegeFilter.appendChild(option);
            });

            const eventTypeFilter = document.getElementById('eventTypeFilter');
            eventTypes.forEach(type => {
                const option = document.createElement('option');
                option.value = type; option.textContent = type;
                eventTypeFilter.appendChild(option);
            });

            [collegeFilter, eventTypeFilter].forEach(el => {
                el.addEventListener('change', () => {
                    filters.college = document.getElementById('collegeFilter').value;
                    filters.type = document.getElementById('eventTypeFilter').value;
                    updateDashboard();
                });
            });

            const chartOptions = (indexAxis = 'x', legendDisplay = false) => ({
                indexAxis, responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: legendDisplay, position: 'top' } },
                scales: { x: { beginAtZero: true }, y: {} }
            });

            popularityChart = new Chart('popularityChart', { type: 'bar', data: {}, options: chartOptions('y') });
            attendanceChart = new Chart('attendanceChart', { type: 'bar', data: {}, options: chartOptions('x', true) });
            feedbackChart = new Chart('feedbackChart', { type: 'doughnut', data: {}, options: { responsive: true, maintainAspectRatio: false } });

            updateDashboard();
        }

        function updateDashboard() {
            const collegeId = filters.college === 'all' ? null : parseInt(filters.college);
            const eventType = filters.type;

            let filteredEvents = mockData.events.filter(e => 
                (collegeId ? e.college_id === collegeId : true) && 
                (eventType !== 'all' ? e.type === eventType : true)
            );
            let eventIds = new Set(filteredEvents.map(e => e.id));
            let filteredRegs = mockData.registrations.filter(r => eventIds.has(r.event_id));
            let filteredAtt = mockData.attendance.filter(a => eventIds.has(a.event_id));
            let filteredFeedback = mockData.feedback.filter(f => eventIds.has(f.event_id));
            
            updateKPIs(filteredEvents, filteredRegs, filteredAtt, filteredFeedback);
            updatePopularityReport(filteredEvents, filteredRegs);
            updateAttendanceChart(filteredEvents, filteredRegs, filteredAtt);
            updateFeedbackChart(filteredFeedback);
            updateStudentParticipationReport(filteredAtt);
        }
        
        function updateKPIs(events, regs, att, feedback) {
            document.getElementById('totalEvents').textContent = events.length.toLocaleString();
            document.getElementById('totalRegistrations').textContent = regs.length.toLocaleString();
            const avgAttendanceRate = regs.length > 0 ? ((att.length / regs.length) * 100).toFixed(1) : 0;
            document.getElementById('avgAttendance').textContent = `${avgAttendanceRate}%`;
            const totalFeedback = feedback.reduce((sum, f) => sum + f.rating, 0);
            const avgFeedbackScore = feedback.length > 0 ? (totalFeedback / feedback.length).toFixed(2) : '0.00';
            document.getElementById('avgFeedback').textContent = `${avgFeedbackScore}/5`;
        }

        function updatePopularityReport(events, regs) {
            const data = events.map(event => ({ name: event.name, count: regs.filter(r => r.event_id === event.id).length }))
                .sort((a, b) => b.count - a.count).slice(0, 10);
            popularityChart.data = {
                labels: data.map(e => e.name).reverse(),
                datasets: [{ label: 'Registrations', data: data.map(e => e.count).reverse(), backgroundColor: '#3b82f6' }]
            };
            popularityChart.update();
        }

        function updateAttendanceChart(events, regs, att) {
            const eventData = events.map(e => ({...e, regCount: regs.filter(r => r.event_id === e.id).length}))
                .sort((a,b) => b.regCount - a.regCount).slice(0, 10);
            
            attendanceChart.data = {
                labels: eventData.map(e => e.name),
                datasets: [
                    { label: 'Registrations', data: eventData.map(e => e.regCount), backgroundColor: 'rgba(59, 130, 246, 0.5)' },
                    { label: 'Attendance', data: eventData.map(e => att.filter(a => a.event_id === e.id).length), backgroundColor: 'rgba(16, 185, 129, 0.7)' }
                ]
            };
            attendanceChart.update();
        }
        
        function updateFeedbackChart(feedback) {
            const ratingCounts = [0, 0, 0, 0, 0]; 
            feedback.forEach(f => ratingCounts[5 - f.rating]++);
            feedbackChart.data = {
                labels: ['5 Stars', '4 Stars', '3 Stars', '2 Stars', '1 Star'],
                datasets: [{ data: ratingCounts, backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#dc2626'] }]
            };
            feedbackChart.update();
        }
        
        function updateStudentParticipationReport(attendance) {
            const studentCounts = {};
            attendance.forEach(att => studentCounts[att.student_id] = (studentCounts[att.student_id] || 0) + 1);
            const sortedStudents = Object.keys(studentCounts).map(id => ({ id: parseInt(id), count: studentCounts[id] }))
                .sort((a, b) => b.count - a.count);
            
            const tableBody = document.getElementById('studentTableBody');
            tableBody.innerHTML = '';
            sortedStudents.slice(0, 50).forEach((s, index) => {
                const student = mockData.students.find(db_s => db_s.id === s.id);
                const isTop3 = index < 3 ? 'bg-amber-100 font-semibold text-amber-800' : '';
                const row = `<tr class="border-b border-slate-200 hover:bg-slate-50 ${isTop3}">
                    <td class="p-3 text-sm text-slate-700">${index + 1}</td>
                    <td class="p-3 text-sm text-slate-700">${student.name}</td>
                    <td class="p-3 text-sm text-slate-700 text-right">${s.count}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        }
        
        window.onload = init;
    </script>
</body>
</html>


const colorArray = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
                '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
                '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
                '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
                '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
                '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
                '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
                '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
                '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
                '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];

function responseToDatasets(response) {
    try {
        chart.options.plugins.title.text = `${response[0].title} - ${document.getElementById("semester").value}`;
    } catch {
        chart.options.plugins.title.text = 'No Data Available for Selection';
    }
    let datasets = [];
    let i = 0;
    for (const section of response) {
        let dataset = {};
        dataset.label = section.section.toString();
        dataset.cubicInterpolationMode = 'monotone';
        dataset.backgroundColor = colorArray[i % colorArray.length];
        dataset.borderColor = colorArray[i++ % colorArray.length];
        dataset.borderWidth = 5;
        dataset.data = [];
        for (const s of section.seats) {
            dataset.data.push({ x: s.d * 86400000 + 28800000, y: s.n });
        }
        datasets.push(dataset);
    }
    return datasets;
}

function updateTable(response) {
    const table = document.getElementById("table");
    while (table.firstChild) table.removeChild(table.firstChild);
    table.className = "table table-hover"; //table-dark
    if (response.length == 0) return;
    table.insertRow().innerHTML = `<th colspan="2">Course</th><th>Instructor</th><th>Number</th><th>Modality</th><th>Times</th><th>Days</th><th>Type</th><th>GE</th><th>Location</th><th>Units</th><th>Dates</th>`
    let i = 0;
    for (const section of response) {
        const bgcolor = `"background-color: ${chart.data.datasets[i].borderColor}"`
        table.insertRow().innerHTML = `
                            <td style=${bgcolor}><input type="checkbox" onclick="toggleDatasetVisibility(${i})" class="form-check-input" checked></td>
                            <td style=${bgcolor}>${section.title}-${section.section}</td>
                            <td>${section.instructor}</td>
                            <td>${section.number}</td>
                            <td>${section.modality}</td>
                            <td>${section.times}</td>
                            <td>${section.days}</td>
                            <td>${section.type}</td>
                            <td>${section.ge}</td>
                            <td>${section.location}</td>
                            <td>${section.units}</td>
                            <td>${section.dates}</td>`;
        i++;
    }
}

function toggleDatasetVisibility(index) {
    chart.setDatasetVisibility(index, !chart.isDatasetVisible(index));
    chart.update();
}

async function fetchSeatData(semester, code) {
    semester = encodeURI(semester);
    code = encodeURI(code);
    return await fetch(`/data?code=${code}&semester=${semester}`).then((response) => response.json());
}

async function fetchCourseCodes() {
    return await fetch(`/coursecodes`).then((response) => response.json());
}

async function fetchSemesters() {
    return await fetch(`/semesters`).then((response) => response.json());
}

function setCourseCodeSelect(options) {
    const select = document.getElementById("courseCodes");
    for (o of options) {
        const opt = document.createElement('option');
        opt.value = o;
        opt.innerText = o;
        select.appendChild(opt);
    }
}

function setSemestersSelect(semesters) {
    const select = document.getElementById("semester");
    for (s of semesters.reverse()) {
        const opt = document.createElement('option');
        opt.value = s;
        opt.innerText = s;
        select.appendChild(opt);
    }
}

function createChart() {
    const cfg = {
        type: 'line',
        data: {
            datasets: []
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Make a Selection Above...',
                    font: {
                        size: 20
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                },
                tooltip: {
                    callbacks: {
                        afterTitle: function (context) {
                            const split = context[0].label.split(",");
                            let label = split[0] + split[1];
                            return label;
                        },
                        title: function (context) {
                            return `${document.getElementById("courseCodes").value}-${context[0].dataset.label}`; //TODO: problem when someone selects a different course but does not press go.
                        },
                        label: function (context) {
                            let label = ` Seats: ${context.parsed.y}`;
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    },
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Seats Remaining'
                    }
                }
            }
        }
    }
    return new Chart(document.getElementById('myChart'), cfg);
}

function updateChart(chart, datasets) {
    chart.data.datasets = datasets;
    chart.update();
}

function initSelects() {
    $('#courseCodes').select2({
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('placeholder'),
    });
    $('#semester').select2({
        theme: "bootstrap-5",
        width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(this).data('placeholder'),
    });
}

function filterData(data)
{
    // Modality Check
    for (let i = 1; i <= 3 ; i++) {
        let modalityCheckBox = document.getElementById("ModalityCheckBox "+i);
        if(modalityCheckBox.checked == false)
        {
            console.log("Enter")
            for (let index = 0; index < data.length; index++) {
                if((data[index].modality).includes(modalityCheckBox.value))
                {
                    data.splice(index,1);
                    index--;
                }
            }
        }
    }
    // Days Check
    for (let i = 1; i <= 5 ; i++) {
        let daysCheckBox = document.getElementById("DaysCheckBox "+i);
        if(daysCheckBox.checked == false)
        {
            for (let index = 0; index < data.length; index++) {
                console.log(data[index].section + " "+data[index].days)
                if((data[index].days).includes(daysCheckBox.value))
                {
                    data.splice(index,1);
                    index--;
                }
            }
        }
    }
    // Times Check
    for (let i = 1; i <= 10 ; i++) {
        let typeCheckBox = document.getElementById("TypeCheckBox "+i);
        if(typeCheckBox.checked == false)
        {
            for (let index = 0; index < data.length; index++) {
                console.log(data[index].type)
                if((data[index].type).includes(typeCheckBox.value))
                {
                    data.splice(index,1);
                    index--;
                }
            }
        }
    }

    return data;
}
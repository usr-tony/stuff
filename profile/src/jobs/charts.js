import customStyles from "../main/custom-styles";

const endpoint =
    "https://g0ud4ex9ui.execute-api.ap-southeast-2.amazonaws.com/jobs";


const backgroundColor = customStyles.bgcolor

const defaultBubbleSeries = (state, setState) => ({
    dataLabels: {
        align: 'center',
        enabled: true,
        format: '{point.name} <br /> {point.value}',
        color: "white",
        style: {
            color: "white",
            textOutline: "none",
            fontFamily: "monospace",
            fontWeight: "normal",
            fontSize: "0.7rem",
        },
    },
    minSize: 15,
    maxSize: 200,
    label: {
        enabled: true,
    },
    events: {
        click: (e) => 
            setState({
                period: "day",
                filters: { [state.by]: e.point.series.name },
                loading: true,
                type: "columns",
            }),
    },
})

export async function bubbles(state, setState) {
    const response = await getData(options(state), setState);
    let data = await response.json()
    const series = []
    for (let row of data) {
        const fullName = row[0]
        if (fullName && state.by != 'state') {
            let words = fullName
                .replace(',', '')
                .split(' ')
            row[0] = words[0] // find another way to modify tooltip and datalabels separately
        }
        series.push({
            ...defaultBubbleSeries(state, setState),
            data: [ row, ],
            name: fullName,
        })
    }
    return {
        title: {
            text: `jobs by ${state.by}`,
            style: {
                font: "13px monospace",
            },
        },
        chart: {
            backgroundColor,
            type: 'packedbubble',
        },
        legend: {
            enabled: false,
        },
        series,
    };
}

export async function columns(state, setState) {
    const response = await getData(options(state), setState);
    const raw = await response.json();
    var data = [];
    var categories = [];
    for (let row of raw) {
        if (!row[0]) {
            row[0] = ''
        }
        if (!state.by) {
            categories.push(formatDate(row[0] * 1000));
        } else {
            categories.push(row[0])
        }
        data.push(row[1]);
    }
    if (state.by) {
        var title = state.by;
    } else {
        const time = state.period == "day" ? "daily" : "weekly";
        var title = `${time} job postings over time`;
        if (state.filters && Object.keys(state.filters).length) {
            const key = Object.keys(state.filters)[0]
            title = `job postings over time where ${key} is ${state.filters[key]}`;
        }
    }
    return {
        title: {
            text: title,
            style: {
                font: "13px monospace",
            },
        },
        chart: {
            backgroundColor,
            type: 'column'
        },
        xAxis: {
            categories,
        },
        legend: {
            enabled: false,
        },
        series: [
            {
                data,
                events: {
                    click: (e) => {
                        if (state.period && Object.keys(state.filters).length) {
                            return
                        }
                        if (!state.by) {
                            return
                        }
                        const name = e.point.category
                        setState({
                            period: "day",
                            filters: { [state.by]: name },
                            loading: true,
                            type: "columns",
                        });
                    },
                },
                tooltip: {
                    // series tooltip options with different options from global
                    pointFormat: '{point.y}',
                },
            },
        ],
        tooltip: {
            // global tooltip options
            enabled: true,
            headerFormat: '',
        },
    };
}

async function getData(options, setState) {
    const response = await fetch(endpoint, options);
    setState((state) => ({
        ...state,
        loading: false,
    }));
    return response;
}

function options(state) {
    return {
        method: "POST",
        mode: "cors",
        body: JSON.stringify(state),
    }
};

function formatDate(ts) {
    return new Date(ts)
        .toLocaleDateString('en-US', {
            weekday: 'short',
            day: 'numeric',
            month: 'short',
        })
}
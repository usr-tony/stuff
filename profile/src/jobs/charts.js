import customStyles from "../main/custom-styles";


const backgroundColor = customStyles.bgcolor

const defaultBubbleSeries = (onClick, showValue) => {
    return {
        dataLabels: {
            align: 'center',
            enabled: true,
            format: showValue ? '{point.name} <br /> {point.value}' : '{point.name}',
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
            click: (e) => onClick(e.point.series.name)
        },
    }
}

export function bubbles(data, onClick, title, showValue=true) {
    /*
    data is a 2d array, of 2 or 3 elements:
    if 3 elements, the last element should be the original name, and the first element is the modified name 
    [name, value] if 2 elements
    [name, modified name, value] if there are 3 in each subarray
    */
    const series = data.map(row => {
        let fullName = row[0]
        if (row.length == 3) {
            row = row.slice(1, 3)
        }
        return { 
            data: [ row, ], 
            name: fullName, 
            ...defaultBubbleSeries(onClick, showValue) 
        }
    })
    return {
        title: {
            text: title,
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
        credits:{
            enabled: false
        },
    };
}

export function columns([ categories, heights ], onClick, title) {
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
                data: heights,
                events: {
                    click: (e) => onClick(e.point.category)
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
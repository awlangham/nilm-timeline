<script>
    import * as d3 from "d3";

    export let nominalValue, actualValue, label;

    const width = 150,
        height = 75;
    const marginLeft = 20,
        marginRight = 20,
        marginTop = 25,
        marginBottom = 40;

    const barWidth = 40;

    const radius = Math.max(width, height) / 2;
    const labelRadius = radius + 5;

    const needleColor = "#444444";

    let lowerBarArc = d3
        .arc()
        .outerRadius(radius)
        .innerRadius(radius - barWidth)
        .cornerRadius(3)
        .startAngle(-Math.PI / 2)
        .endAngle(-Math.PI / 4);

    let upperBarArc = d3
        .arc()
        .outerRadius(radius)
        .innerRadius(radius - barWidth)
        .cornerRadius(3)
        .startAngle(Math.PI / 4)
        .endAngle(Math.PI / 2);

    let greenBarArc = d3
        .arc()
        .outerRadius(radius)
        .innerRadius(radius - barWidth)
        .cornerRadius(3)
        .startAngle(-Math.PI / 4)
        .endAngle(Math.PI / 4);

    let labelsArc = d3
        .arc()
        .outerRadius(labelRadius)
        .innerRadius(labelRadius)
        .startAngle(-Math.PI / 2)
        .endAngle(Math.PI / 2);

    let needle;

    $: d3.select(needle)
        .transition()
        .duration(500)
        .ease(d3.easeCubic)
        .attr("transform", "rotate(" + theta + ")");

    $: upperBound = Math.max(1.5 * nominalValue, nominalValue + 5);
    $: lowerBound = Math.min(0.5 * nominalValue, nominalValue - 5);

    $: angleScale = d3
        .scaleLinear()
        .domain([lowerBound, nominalValue, upperBound])
        .range([45, 90, 135]);
    $: theta = angleScale(actualValue);
</script>

<svg
    id="gauge"
    width={width + marginLeft + marginRight}
    height={height + marginTop + marginBottom}
>
    <g transform="translate({width / 2 + marginLeft}, {height + marginTop})">
        <path d={lowerBarArc()} fill="yellow" stroke={needleColor}></path>
        <path d={upperBarArc()} fill="yellow" stroke={needleColor}></path>
        <path d={greenBarArc()} fill="green" stroke={needleColor}></path>
        <path id="labelsArc" d={labelsArc()}></path>
        <circle cx="0" cy="0" r="15" fill={needleColor}></circle>
        <path
            bind:this={needle}
            fill={needleColor}
            d="M 0 15 L {-0.9 * radius} 0 L 0 -15"
        ></path>
        <text>
            <textPath
                href="#labelsArc"
                startOffset={(Math.PI * labelRadius) / 4}
                text-anchor="middle"
            >
                {lowerBound.toFixed(0)}
            </textPath>

            <textPath
                href="#labelsArc"
                startOffset={(Math.PI * labelRadius) / 2}
                text-anchor="middle"
            >
                {nominalValue.toFixed(0)}
            </textPath>

            <textPath
                href="#labelsArc"
                startOffset={(3 * Math.PI * labelRadius) / 4}
                text-anchor="middle"
            >
                {upperBound.toFixed(0)}
            </textPath>
        </text>

        <text transform="translate(0, 30)" text-anchor="middle">{label}</text>
    </g>
</svg>

<style>
    #gauge {
        border: 2px solid gray;
        border-radius: 10px;
        box-shadow: 3px 1px 4px #888;
    }
</style>

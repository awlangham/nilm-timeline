<script>
    import * as d3 from "d3";

    export let observed, nominal, threshold;

    const width = 180,
        height = 180;
    const marginLeft = 20,
        marginRight = 5,
        marginTop = 5,
        marginBottom = 30;

    const observedMag = Math.sqrt(observed[0] ** 2 + observed[1] ** 2);
    const nominalMag = Math.sqrt(nominal[0] ** 2 + nominal[1] ** 2);
    const axisExtent = 1.1 * Math.max(observedMag, nominalMag);

    const xMin = -axisExtent,
        xMax = axisExtent,
        yMin = -axisExtent,
        yMax = axisExtent;

    const xAxisScale = d3.scaleLinear(
        [xMin, xMax],
        [marginLeft, marginLeft + width],
    );

    const yAxisScale = d3.scaleLinear(
        [yMin, yMax],
        [marginTop + height, marginTop],
    );
</script>

<svg
    id="gauge"
    width={width + marginLeft + marginRight}
    height={height + marginTop + marginBottom}
>
    <defs>
        <marker
            id="observedArrow"
            viewBox="0 0 10 10"
            refX="5"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            fill="black"
            orient="auto-start-reverse"
        >
            <path d="M 0 0 L 10 5 L 0 10 z" />
        </marker>

        <marker
            id="nominalArrow"
            viewBox="0 0 10 10"
            refX="5"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            fill="#C0C0C0"
            orient="auto-start-reverse"
        >
            <path d="M 0 0 L 10 5 L 0 10 z" />
        </marker>
    </defs>

    <ellipse
        cx={xAxisScale(nominal[0])}
        cy={yAxisScale(nominal[1])}
        rx={xAxisScale(nominal[0] + threshold) - xAxisScale(nominal[0])}
        ry={yAxisScale(nominal[1] + threshold) - yAxisScale(nominal[1])}
        fill="green"
        fill-opacity="0.5"
    ></ellipse>

    <line
        x1={marginLeft + width / 2}
        y1={marginTop}
        x2={marginLeft + width / 2}
        y2={height + marginTop}
        stroke="black"
        opacity="0.2"
    />

    <line
        x1={marginLeft}
        y1={marginTop + height / 2}
        x2={width + marginLeft}
        y2={marginTop + height / 2}
        stroke="black"
        opacity="0.2"
    />

    <line
        x1={xAxisScale(0)}
        y1={yAxisScale(0)}
        x2={xAxisScale(nominal[0])}
        y2={yAxisScale(nominal[1])}
        stroke="#C0C0C0"
        stroke-width="2.5"
        marker-end="url(#nominalArrow)"
    />

    <line
        x1={xAxisScale(0)}
        y1={yAxisScale(0)}
        x2={xAxisScale(observed[0])}
        y2={yAxisScale(observed[1])}
        stroke="black"
        stroke-width="2.5"
        marker-end="url(#observedArrow)"
    />

    <text
        x={xAxisScale(0)}
        y={marginTop + height + marginBottom - 5}
        text-anchor="middle">In-Phase</text
    >

    <text
        transform="rotate(-90, 5, {yAxisScale(0)})"
        x={5}
        y={yAxisScale(0)}
        dominant-baseline="hanging"
        text-anchor="middle">Quadrature</text
    >
</svg>

<style>
    #gauge {
        border: 2px solid gray;
        border-radius: 10px;
        box-shadow: 3px 1px 4px #888;
        margin-top: 20px;
    }
</style>

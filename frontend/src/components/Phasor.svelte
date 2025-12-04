<script>
    import * as d3 from "d3";

    export let observed, nominal;

    const width = 150,
        height = 150;
    const marginLeft = 5,
        marginRight = 5,
        marginTop = 5,
        marginBottom = 5;

    const xMin = -0.1,
        xMax = 0.1,
        yMin = -0.1,
        yMax = 0.1;

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
            id="arrow"
            viewBox="0 0 10 10"
            refX="5"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
        >
            <path d="M 0 0 L 10 5 L 0 10 z" />
        </marker>
    </defs>
    <line
        x1={marginLeft + width / 2}
        y1={marginTop}
        x2={marginLeft + width / 2}
        y2={height + marginTop}
        stroke="black"
    />

    <line
        x1={marginLeft}
        y1={marginTop + height / 2}
        x2={width + marginLeft}
        y2={marginTop + height / 2}
        stroke="black"
    />

    <line
        x1={xAxisScale(0)}
        y1={yAxisScale(0)}
        x2={xAxisScale(observed[0])}
        y2={yAxisScale(observed[1])}
        stroke="black"
        stroke-width="2"
        marker-end="url(#arrow)"
    />

    <line
        x1={xAxisScale(0)}
        y1={yAxisScale(0)}
        x2={xAxisScale(nominal[0])}
        y2={yAxisScale(nominal[1])}
        stroke="black"
        stroke-width="2"
        marker-end="url(#arrow)"
    />
</svg>

{observed}

<style>
    #gauge {
        border: 2px solid gray;
        border-radius: 10px;
        box-shadow: 3px 1px 4px #888;
        margin-top: 20px;
    }
</style>

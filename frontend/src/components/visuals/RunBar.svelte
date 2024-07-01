<script>
    import { createEventDispatcher } from "svelte";

    export let start_x, end_x, y, height, fill, distance;

    let bar;

    const dispatch = createEventDispatcher();

    const runSelected = () => {
        //     d3.select(bar)
        //         .raise()
        //         .transition()
        //         .duration(400)
        //         .attr("transform", "translate(0, 0)")
        //         .attr("height", 1000)
        //         .attr("width", 3000)
        //         .attr("fill", "white")
        //         .on("end", () => {
        //             dispatch("select");
        //         });
        dispatch("select");
    };
</script>

<rect
    bind:this={bar}
    transform="translate({start_x}, {y})"
    {height}
    width={Math.max(2, end_x - start_x)}
    {fill}
    opacity={1 - distance}
    rx="10"
    ry="10"
    on:click={runSelected}
    on:keypress={runSelected}
    role="button"
    tabindex="0"
    style="stroke-opacity: {Math.min(100, 10 * (end_x - start_x))}%"
/>

<style>
    rect {
        stroke-width: 2px;
        stroke: rgb(27, 27, 27);
        cursor: pointer;
    }
</style>

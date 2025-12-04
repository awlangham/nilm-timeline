<script>
    import { createEventDispatcher } from "svelte";

    export let start_x, end_x, y, height, fill, faulty;

    const dispatch = createEventDispatcher();

    const runSelected = () => {
        dispatch("select");
    };
</script>

<rect
    transform="translate({start_x}, {y})"
    {height}
    width={Math.max(2, end_x - start_x)}
    fill={faulty ? 'red' : fill}
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

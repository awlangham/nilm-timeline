<script>
    import { fade } from "svelte/transition";

    export let x, y;
</script>

<text {x} {y} text-anchor="middle" out:fade>
    <slot />
</text>

<style>
    text {
        font-family: sans-serif;
        font-size: 24px;
    }
</style>

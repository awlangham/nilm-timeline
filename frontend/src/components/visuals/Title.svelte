<script>
    export let x, y;
</script>

<text {x} {y} text-anchor="middle">
    <slot />
</text>

<style>
    text {
        font-family: sans-serif;
        font-size: 24px;
    }
</style>

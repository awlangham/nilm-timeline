<script>
    import EventView from "./views/EventView.svelte";
    import TimelineView from "./views/TimelineView.svelte";
    import { fade } from "svelte/transition";

    let selectedInterval = [];
    const fadeConfig = { duration: 200 };
</script>

<div class="main">
    <div hidden={selectedInterval.length != 0}>
        <TimelineView bind:selectedInterval />
    </div>

    {#if selectedInterval.length != 0}
        <div
            hidden={selectedInterval.length === 0}
            transition:fade={fadeConfig}
        >
            <EventView bind:selectedInterval />
        </div>
    {/if}
</div>

<style>
    .main {
        display: grid;
    }

    .main > * {
        grid-area: 1 / 1;
    }
</style>

<script>
    import EventView from "./views/EventView.svelte";
    import TimelineView from "./views/TimelineView.svelte";
    import { fade } from "svelte/transition";

    let selectedTimestamp = -1;
    const fadeConfig = { duration: 250 };
</script>

<div class="main">
    {#if selectedTimestamp === -1}
        <div transition:fade={fadeConfig}>
            <TimelineView bind:selectedTimestamp />
        </div>
    {:else}
        <div transition:fade={fadeConfig}>
            <EventView bind:selectedTimestamp />
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

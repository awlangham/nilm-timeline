<script>
    import EventView from "./views/EventView.svelte";
    import TimelineView from "./views/TimelineView.svelte";

    let selectedTimestamp = -1;
</script>

{#if selectedTimestamp === -1}
    <TimelineView bind:selectedTimestamp />
{:else}
    <EventView bind:selectedTimestamp />
{/if}

<script>
    import EventView from "./views/EventView.svelte";
    import TimelineView from "./views/TimelineView.svelte";

    let selectedID = -1;
</script>

{#if selectedID === -1}
    <TimelineView bind:selectedID />
{:else}
    <EventView bind:selectedID />
{/if}

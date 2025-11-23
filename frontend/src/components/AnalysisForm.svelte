<script>
  export let onSubmit;

  let address = '';
  let isSubmitting = false;

  const handleSubmit = async () => {
    if (!address.trim()) {
      return;
    }
    isSubmitting = true;
    await onSubmit(address);
    isSubmitting = false;
  };
</script>

<div class="w-full max-w-md mx-auto">
  <form
    on:submit|preventDefault={handleSubmit}
    class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
  >
    <div class="mb-4">
      <label
        for="address"
        class="block text-gray-700 text-sm font-bold mb-2"
      >
        Adresse à analyser
      </label>
      <input
        id="address"
        type="text"
        bind:value={address}
        placeholder="Ex: 123 Rue de la République, 75001 Paris"
        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        disabled={isSubmitting}
      />
    </div>
    <div class="flex items-center justify-center">
      <button
        type="submit"
        disabled={isSubmitting || !address.trim()}
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {#if isSubmitting}
          Analyse en cours...
        {:else}
          Lancer l'analyse
        {/if}
      </button>
    </div>
  </form>
</div>







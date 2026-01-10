<script>
  import { MapboxSearchBox } from '@mapbox/search-js-web';
  import { onDestroy, onMount } from 'svelte';
  import { link } from 'svelte-spa-router';
  import { getCityInformation } from '../lib/api.js';

  let address = '';
  let loading = false;
  let error = null;
  let result = null;
  let searchBoxContainer;
  let searchBox;
  let mapboxConfigured = true;

  onMount(async () => {
    if (!searchBoxContainer) return;
    
    const mapboxToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;
    
    if (!mapboxToken) {
      mapboxConfigured = false;
      error = 'La clé API Mapbox n\'est pas configurée. Veuillez ajouter VITE_MAPBOX_ACCESS_TOKEN dans votre fichier .env du frontend. Consultez le README pour plus d\'informations.';
      console.warn('VITE_MAPBOX_ACCESS_TOKEN n\'est pas configuré. Veuillez ajouter votre clé Mapbox dans un fichier .env');
      return;
    }

    // S'assurer que le conteneur est vide avant d'ajouter le widget (éviter les doublons)
    if (searchBoxContainer.hasChildNodes()) {
      searchBoxContainer.innerHTML = '';
    }

    // Attendre que le DOM soit complètement rendu
    await new Promise(resolve => setTimeout(resolve, 0));

    // Ne créer le widget qu'une seule fois
    if (!searchBox || !searchBoxContainer.contains(searchBox)) {
      searchBox = new MapboxSearchBox();
      searchBox.accessToken = mapboxToken;
      searchBox.options = {
        language: 'fr',
        country: 'FR'
      };
      searchBox.placeholder = 'Entrez une adresse (ex: 15 rue de la Paix, Paris)';
      searchBox.interceptSearch = (val) => {
        if (val && val.trim().length >= 3) {
          return val.trim();
        }
        return null;
      };

      // Configuration du popover pour que les suggestions s'affichent correctement
      // Note: Le widget utilise floating-ui pour positionner les suggestions
      searchBox.popoverOptions = {
        placement: 'bottom-start',
        flip: true,
        shift: false,
        offset: 8
      };

      // Configuration du thème pour correspondre au design sombre
      // Note: Le widget Mapbox utilise Shadow DOM, donc les styles doivent être appliqués via le thème
      searchBox.theme = {
        variables: {
          colorPrimary: '#06b6d4',
          colorPrimaryFocus: '#0891b2',
          colorBackground: '#1e293b',
          colorBackgroundHover: '#334155',
          colorText: '#f1f5f9',
          colorTextSecondary: '#94a3b8',
          colorBorder: '#475569',
          borderRadius: '0px'
        },
        cssText: `
          :host {
            display: block !important;
            width: 100% !important;
            min-height: 80px !important;
            position: relative !important;
          }
          .Input {
            background-color: transparent !important;
            color: #f1f5f9 !important;
            border: none !important;
            padding: 1.25rem 1rem !important;
            font-size: 1.125rem !important;
            width: 100% !important;
            box-sizing: border-box !important;
            outline: none !important;
          }
          .Input::placeholder {
            color: #64748b !important;
            opacity: 1 !important;
          }
          .Input:focus {
            outline: none !important;
            box-shadow: none !important;
          }
          .Listbox {
            background-color: #1e293b !important;
            border: 1px solid #475569 !important;
            border-radius: 12px !important;
            margin-top: 0.5rem !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3) !important;
            z-index: 10000 !important;
            max-height: 400px !important;
            overflow-y: auto !important;
            padding: 0.5rem 0 !important;
            position: absolute !important;
            top: 100% !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            margin-top: 0.5rem !important;
          }
          .ListboxOption {
            color: #f1f5f9 !important;
            padding: 0.875rem 1.25rem !important;
            cursor: pointer !important;
            transition: background-color 0.15s ease !important;
          }
          .ListboxOption:hover {
            background-color: #334155 !important;
          }
          .ListboxOption[aria-selected="true"] {
            background-color: rgba(6, 182, 212, 0.2) !important;
            border-left: 3px solid #06b6d4 !important;
          }
          .ListboxOption[aria-selected="true"]:hover {
            background-color: rgba(6, 182, 212, 0.3) !important;
          }
          .ListboxOptionText {
            color: #f1f5f9 !important;
            font-size: 1rem !important;
          }
          .ListboxOptionTextSecondary {
            color: #94a3b8 !important;
            font-size: 0.875rem !important;
          }
        `
      };

      // Gestionnaire d'événement pour la sélection d'une adresse
      searchBox.addEventListener('retrieve', async (e) => {
        try {
          const response = e.detail;
          let selectedAddress = '';
          
          // La réponse de MapboxSearchBox est une SearchBoxRetrieveResponse
          // qui contient une FeatureCollection avec les features
          if (response && response.features && Array.isArray(response.features) && response.features.length > 0) {
            const feature = response.features[0];
            // Utiliser full_address qui contient l'adresse complète formatée
            selectedAddress = feature.properties?.full_address || 
                            feature.properties?.place_formatted || 
                            feature.properties?.name || 
                            searchBox.value || '';
          } else {
            // Fallback sur la valeur du champ
            selectedAddress = searchBox.value || '';
          }
          
          if (selectedAddress && selectedAddress.trim()) {
            address = selectedAddress.trim();
            // Déclencher automatiquement la recherche
            await handleSubmit();
          }
        } catch (err) {
          console.error('Erreur lors de la récupération de l\'adresse:', err);
          // En cas d'erreur, utiliser au moins la valeur du champ
          const currentValue = searchBox?.value || '';
          if (currentValue.trim()) {
            address = currentValue.trim();
          }
        }
      });

      // Mise à jour de la variable address quand l'utilisateur tape
      searchBox.addEventListener('input', (e) => {
        if (e.target === searchBox.input) {
          address = searchBox.value;
        }
      });

      // Ajouter le widget au conteneur (une seule fois)
      if (searchBoxContainer && !searchBoxContainer.contains(searchBox)) {
        searchBoxContainer.appendChild(searchBox);
      }
    }
  });

  onDestroy(() => {
    if (searchBox && searchBoxContainer) {
      // Supprimer le widget du DOM et nettoyer
      if (searchBox.parentNode === searchBoxContainer) {
        searchBoxContainer.removeChild(searchBox);
      }
      // Nettoyer les event listeners si nécessaire
      searchBox = null;
    }
  });

  const handleSubmit = async () => {
    if (!address.trim()) return;
    
    loading = true;
    error = null;
    result = null;

    try {
      result = await getCityInformation(address);
    } catch (err) {
      error = err.response?.data?.detail || err.message || 'Erreur lors de la récupération des informations';
      console.error('Error fetching city information:', err);
    } finally {
      loading = false;
    }
  };

  const getPoliticalColor = (color) => {
    const colors = {
      'gauche': { bg: 'bg-rose-500', text: 'text-rose-500', border: 'border-rose-500', light: 'bg-rose-50' },
      'droite': { bg: 'bg-blue-600', text: 'text-blue-600', border: 'border-blue-600', light: 'bg-blue-50' },
      'centre': { bg: 'bg-amber-500', text: 'text-amber-500', border: 'border-amber-500', light: 'bg-amber-50' },
      'ecolo': { bg: 'bg-emerald-500', text: 'text-emerald-500', border: 'border-emerald-500', light: 'bg-emerald-50' },
      'vert': { bg: 'bg-emerald-500', text: 'text-emerald-500', border: 'border-emerald-500', light: 'bg-emerald-50' },
    };
    
    const lowerColor = color?.toLowerCase() || '';
    for (const [key, value] of Object.entries(colors)) {
      if (lowerColor.includes(key)) return value;
    }
    return { bg: 'bg-slate-500', text: 'text-slate-500', border: 'border-slate-500', light: 'bg-slate-50' };
  };

  const formatPresentation = (text) => {
    if (!text) return [];
    return text.split('\n').filter(p => p.trim());
  };
</script>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
  <!-- Navigation -->
  <nav class="border-b border-slate-700/50 backdrop-blur-sm bg-slate-900/50 sticky top-0 z-50">
    <div class="container mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        <a href="/" use:link class="flex items-center gap-3 group">
          <div class="w-10 h-10 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:shadow-cyan-500/40 transition-shadow">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
            </svg>
          </div>
          <span class="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">AgentImmo</span>
        </a>
        <div class="flex items-center gap-2">
          <span class="px-3 py-1.5 text-xs font-medium bg-cyan-500/10 text-cyan-400 rounded-full border border-cyan-500/20">
            City Information
          </span>
        </div>
      </div>
    </div>
  </nav>

  <main class="container mx-auto px-6 py-12">
    <!-- Header -->
    <header class="text-center mb-12">
      <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">
        <span class="bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
          Informations Ville
        </span>
      </h1>
      <p class="text-slate-400 text-lg max-w-2xl mx-auto">
        Obtenez des informations détaillées sur n'importe quelle ville en France : situation géographique, orientation politique et présentation qualitative.
      </p>
    </header>

    <!-- Search Form -->
    <div class="max-w-2xl mx-auto mb-12 search-form-wrapper">
      {#if mapboxConfigured}
        <form on:submit|preventDefault={handleSubmit} class="relative">
          <div class="relative group">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl blur opacity-30 group-hover:opacity-50 transition duration-300"></div>
            <div class="relative bg-slate-800 rounded-2xl border border-slate-700/50 overflow-visible">
              <div class="flex items-stretch min-h-[80px]">
                <div class="flex items-center justify-center pl-5 text-slate-400 flex-shrink-0 z-10">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="flex-1 relative min-h-[80px]" bind:this={searchBoxContainer} style="overflow: visible;">
                  <!-- Le widget Mapbox sera injecté ici -->
                </div>
                <button
                  type="submit"
                  disabled={loading || !address.trim()}
                  class="px-8 py-5 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold hover:from-cyan-400 hover:to-blue-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center gap-2 flex-shrink-0 rounded-r-2xl z-10"
                >
                  {#if loading}
                    <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Analyse...</span>
                  {:else}
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                    </svg>
                    <span>Analyser</span>
                  {/if}
                </button>
              </div>
            </div>
          </div>
        </form>
      {:else}
        <!-- Fallback si Mapbox n'est pas configuré -->
        <form on:submit|preventDefault={handleSubmit} class="relative">
          <div class="relative group">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl blur opacity-30 group-hover:opacity-50 transition duration-300"></div>
            <div class="relative flex bg-slate-800 rounded-2xl overflow-hidden border border-slate-700/50">
              <div class="flex items-center pl-5 text-slate-400 flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                </svg>
              </div>
              <input
                type="text"
                bind:value={address}
                placeholder="Entrez une adresse (ex: 15 rue de la Paix, Paris)"
                class="flex-1 px-4 py-5 bg-transparent text-white placeholder-slate-500 focus:outline-none text-lg"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !address.trim()}
                class="px-8 py-5 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold hover:from-cyan-400 hover:to-blue-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center gap-2"
              >
                {#if loading}
                  <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Analyse...</span>
                {:else}
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                  </svg>
                  <span>Analyser</span>
                {/if}
              </button>
            </div>
          </div>
        </form>
      {/if}
    </div>

    <!-- Error Display -->
    {#if error}
      <div class="max-w-2xl mx-auto mb-8">
        <div class="bg-red-500/10 border border-red-500/30 rounded-xl p-5 flex items-start gap-4">
          <div class="flex-shrink-0 w-10 h-10 bg-red-500/20 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </div>
          <div>
            <h3 class="text-red-400 font-semibold mb-1">Erreur</h3>
            <p class="text-red-300/80">{error}</p>
          </div>
        </div>
      </div>
    {/if}

    <!-- Results Display -->
    {#if result?.city_information}
      {@const cityInfo = result.city_information}
      {@const politicalStyle = getPoliticalColor(cityInfo.politique_color)}
      
      <div class="max-w-5xl mx-auto space-y-6 animate-fade-in">
        <!-- Address Banner -->
        <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-cyan-500/10 via-blue-500/10 to-purple-500/10 border border-slate-700/50 p-6">
          <div class="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl"></div>
          <div class="relative flex items-center gap-4">
            <div class="w-14 h-14 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div>
              <p class="text-slate-400 text-sm font-medium uppercase tracking-wider">Adresse analysée</p>
              <h2 class="text-2xl font-bold text-white">{result.adress_in}</h2>
            </div>
          </div>
        </div>

        <!-- Info Cards Grid -->
        <div class="grid md:grid-cols-2 gap-6">
          <!-- Situation Card -->
          <div class="group relative overflow-hidden rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 hover:border-cyan-500/30 transition-colors duration-300">
            <div class="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 rounded-full blur-2xl group-hover:bg-cyan-500/10 transition-colors"></div>
            <div class="relative">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-10 h-10 bg-cyan-500/20 rounded-lg flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-cyan-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M12 1.586l-4 4v12.828l4-4V1.586zM3.707 3.293A1 1 0 002 4v10a1 1 0 00.293.707L6 18.414V5.586L3.707 3.293zM17.707 5.293L14 1.586v12.828l2.293 2.293A1 1 0 0018 16V6a1 1 0 00-.293-.707z" clip-rule="evenodd" />
                  </svg>
                </div>
                <h3 class="text-lg font-semibold text-white">Situation</h3>
              </div>
              <p class="text-slate-300 leading-relaxed">{cityInfo.situation || 'Non disponible'}</p>
            </div>
          </div>

          <!-- Political Color Card -->
          <div class="group relative overflow-hidden rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 hover:border-purple-500/30 transition-colors duration-300">
            <div class="absolute top-0 right-0 w-32 h-32 bg-purple-500/5 rounded-full blur-2xl group-hover:bg-purple-500/10 transition-colors"></div>
            <div class="relative">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-purple-400" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
                  </svg>
                </div>
                <h3 class="text-lg font-semibold text-white">Orientation Politique</h3>
              </div>
              {#if cityInfo.politique_color}
                <div class="inline-flex items-center gap-2 px-4 py-2 {politicalStyle.light} rounded-full border {politicalStyle.border}">
                  <span class="w-3 h-3 {politicalStyle.bg} rounded-full"></span>
                  <span class="{politicalStyle.text} font-medium">{cityInfo.politique_color}</span>
                </div>
              {:else}
                <p class="text-slate-400">Non disponible</p>
              {/if}
            </div>
          </div>
        </div>

        <!-- Qualitative Presentation Card -->
        {#if cityInfo.qualitative_presentation}
          <div class="group relative overflow-hidden rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 hover:border-emerald-500/30 transition-colors duration-300">
            <div class="absolute top-0 right-0 w-48 h-48 bg-emerald-500/5 rounded-full blur-3xl group-hover:bg-emerald-500/10 transition-colors"></div>
            <div class="relative">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 bg-emerald-500/20 rounded-lg flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                  </svg>
                </div>
                <h3 class="text-lg font-semibold text-white">Présentation Qualitative</h3>
              </div>
              <div class="prose prose-invert prose-slate max-w-none">
                {#each formatPresentation(cityInfo.qualitative_presentation) as paragraph}
                  <p class="text-slate-300 leading-relaxed mb-4 last:mb-0">{paragraph}</p>
                {/each}
              </div>
            </div>
          </div>
        {/if}
      </div>
    {/if}

    <!-- Empty State -->
    {#if !result && !loading && !error}
      <div class="text-center py-16">
        <div class="w-24 h-24 mx-auto mb-6 bg-slate-800/50 rounded-full flex items-center justify-center border border-slate-700/50">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-slate-400 mb-2">Recherchez une adresse</h3>
        <p class="text-slate-500 max-w-md mx-auto">
          Entrez une adresse française pour obtenir des informations détaillées sur la ville correspondante.
        </p>
      </div>
    {/if}
  </main>
</div>

<style>
  @keyframes fade-in {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .animate-fade-in {
    animation: fade-in 0.5s ease-out;
  }

  .prose p {
    white-space: pre-wrap;
  }

  /* Styles pour l'intégration du widget Mapbox */
  .search-form-wrapper {
    position: relative;
    z-index: 10;
  }

  /* Permettre l'overflow visible pour que les suggestions s'affichent */
  .search-form-wrapper :global(.relative.group) {
    overflow: visible !important;
  }

  .search-form-wrapper :global(.relative.bg-slate-800) {
    overflow: visible !important;
  }

  /* Style pour le widget Mapbox - s'assurer qu'il n'y a pas de duplication */
  .search-form-wrapper :global([data-mapbox-search-box]),
  .search-form-wrapper :global(mapbox-search-box) {
    width: 100% !important;
    min-height: 80px !important;
    display: block !important;
    flex: 1 1 auto !important;
    position: relative !important;
  }

  /* S'assurer que le conteneur du widget n'a pas d'overflow et qu'il ne crée pas de duplication */
  .search-form-wrapper :global(.flex-1.relative) {
    overflow: visible !important;
    position: relative !important;
    flex: 1 1 auto !important;
  }

  /* Empêcher la duplication des inputs dans le Shadow DOM */
  .search-form-wrapper :global([data-mapbox-search-box]::part(input)),
  .search-form-wrapper :global(mapbox-search-box::part(input)) {
    display: block !important;
  }
</style>



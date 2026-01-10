<script>
  import Router from 'svelte-spa-router';
  import Home from './pages/Home.svelte';
  import CityInformation from './pages/CityInformation.svelte';

  const routes = {
    '/': Home,
    '/city-information': CityInformation,
  };
</script>

<Router {routes} />

<style>
  :global(body) {
    margin: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
</style>

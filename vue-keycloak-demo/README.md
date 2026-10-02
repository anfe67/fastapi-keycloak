# Vue Keycloak Demo

A Vue 3 frontend demo application demonstrating Keycloak authentication integration with the FastAPI backend.

## Overview

This demo application showcases:
- Keycloak authentication using `keycloak-js`
- Vue 3 with TypeScript and Vite
- Pinia for state management
- Vue Router for navigation
- Axios for API communication with the FastAPI backend

## Prerequisites

- Node.js ^22.18.0 || >=24.12.0
- npm
- Running FastAPI backend (see parent project README)
- Running Keycloak instance (see parent project README)

## Installation

```sh
npm install
```

## Development

Start the development server with hot-reload:

```sh
npm run dev
```

The application will be available at `http://localhost:5173` (or the port shown in terminal).

## Build for Production

Type-check and build the application:

```sh
npm run build
```

Preview the production build:

```sh
npm run preview
```

## Code Formatting

Format the code using Prettier:

```sh
npm run format
```

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Browser DevTools

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Configuration

See [Vite Configuration Reference](https://vite.dev/config/).

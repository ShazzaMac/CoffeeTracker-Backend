const reportWebVitals = (onPerfEntry) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import("web-vitals").then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export default reportWebVitals;

//default setup in React projects created with Create React App (CRA). It is used to measure and report web performance metrics in your application
//It uses the web-vitals library to measure and report performance metrics in your application.
/*
Purpose:

This file helps measure Core Web Vitals, which are key metrics defined by Google to assess user experience. These include:
CLS (Cumulative Layout Shift): Measures visual stability.
FID (First Input Delay): Measures interactivity.
FCP (First Contentful Paint): Measures time to render the first visible content.
LCP (Largest Contentful Paint): Measures loading performance.
TTFB (Time to First Byte): Measures server response time.
How It Works:

If onPerfEntry (a callback function) is provided and is a valid function, it dynamically imports the web-vitals library.
It then runs functions like getCLS, getFID, etc., to calculate and pass the respective metrics to onPerfEntry.
Dynamic Import:

The import('web-vitals') is used to load the web-vitals library only when needed, keeping the main bundle size smaller.

*/

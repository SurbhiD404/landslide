function App() {
  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: "1rem" }}>
      <h1>Landslide EWS — Field App</h1>
      <p>Offline-first reporting for field officials and citizens.</p>

      <section style={{ marginTop: "1.5rem", padding: "1rem", border: "1px solid #ccc", borderRadius: "8px" }}>
        <h3>Report Form (Phase 4)</h3>
        <ul>
          <li>Geo-tagged photo/video capture</li>
          <li>Report type: crack, slope movement, road blocked</li>
          <li>Description field</li>
          <li>IndexedDB offline queue with background sync</li>
        </ul>
      </section>

      <section style={{ marginTop: "1.5rem", padding: "1rem", border: "1px solid #ccc", borderRadius: "8px" }}>
        <h3>Alert Feed (Phase 5)</h3>
        <ul>
          <li>Multilingual alerts (EN/AS/BN)</li>
          <li>Push notifications via FCM</li>
          <li>Risk level display</li>
        </ul>
      </section>
    </div>
  );
}

export default App;

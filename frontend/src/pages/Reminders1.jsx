export default function Reminders() {
  return (
    <div className="container">
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h2>Deadline Reminders</h2>
        <p style={{ marginBottom: '2rem' }}>
          Never miss a scholarship deadline. We'll notify you well in advance.
        </p>
        
        <div className="card">
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '1rem',
            marginBottom: '1.5rem'
          }}>
            <div style={{
              width: '60px',
              height: '60px',
              background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem'
            }}>⏰</div>
            <div>
              <h3 style={{ margin: 0 }}>Coming Soon</h3>
              <p style={{ margin: 0, color: '#64748b' }}>Smart deadline tracking system</p>
            </div>
          </div>
          
          <p>
            We're building an intelligent reminder system that will:
          </p>
          
          <ul>
            <li><strong>Email & SMS Alerts</strong> - Get notified 7 days before deadlines</li>
            <li><strong>Application Progress Tracking</strong> - Monitor your submission status</li>
            <li><strong>Document Checklist</strong> - Know exactly what you need to submit</li>
            <li><strong>WhatsApp Integration</strong> - Receive reminders on WhatsApp</li>
            <li><strong>Calendar Sync</strong> - Add deadlines to your calendar automatically</li>
          </ul>
          
          <div style={{ 
            marginTop: '2rem',
            padding: '1rem',
            background: '#f0f9ff',
            borderRadius: '8px',
            borderLeft: '4px solid #0ea5e9'
          }}>
            <p style={{ margin: 0, fontSize: '0.95rem' }}>
              <strong>📞 For Rural Students:</strong> We're working with schools to send 
              physical reminder letters for students without smartphones or internet access.
            </p>
          </div>
        </div>
        
        <div style={{ 
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '1.5rem',
          marginTop: '3rem'
        }}>
          <div className="card">
            <h4>📱 SMS Reminders</h4>
            <p>Basic phone? We'll send SMS alerts for important deadlines.</p>
          </div>
          
          <div className="card">
            <h4>🏫 School Notices</h4>
            <p>We'll coordinate with schools to display deadline notices on notice boards.</p>
          </div>
          
          <div className="card">
            <h4>📧 Email Digest</h4>
            <p>Weekly email with all upcoming deadlines and application tips.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
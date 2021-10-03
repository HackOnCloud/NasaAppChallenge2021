import { useEffect } from 'react';

export function SolarIrradianceByMonth() {
  useEffect(() => {
    var divElement = document.getElementById('viz1633248269750');
    var vizElement = divElement.getElementsByTagName('object')[0];
    if (divElement.offsetWidth > 800) {
      vizElement.style.minWidth = '420px';
      vizElement.style.maxWidth = '1920px';
      vizElement.style.width = '100%';
      vizElement.style.height = '427px';
    } else if (divElement.offsetWidth > 500) {
      vizElement.style.minWidth = '420px';
      vizElement.style.maxWidth = '1920px';
      vizElement.style.width = '100%';
      vizElement.style.height = '427px';
    } else {
      vizElement.style.width = '100%';
      vizElement.style.height = divElement.offsetWidth * 1.77 + 'px';
    }
    var scriptElement = document.createElement('script');
    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
    vizElement.parentNode.insertBefore(scriptElement, vizElement);
  }, []);

  return (
    <div>
      <div className="tableauPlaceholder" id="viz1633248269750" style={{ position: 'relative' }}>
        <noscript>
          <a href="#">
            <img
              alt="Irradiance by Month at Your Location Dashboard-No Header "
              src="https://public.tableau.com/static/images/TR/TR8KH6XPZ/1_rss.png"
              style={{ border: 'none' }}
            />
          </a>
        </noscript>
        <object className="tableauViz" style={{ display: 'none' }}>
          <param name="host_url" value="https%3A%2F%2Fpublic.tableau.com%2F" />{' '}
          <param name="embed_code_version" value="3" /> <param name="path" value="shared/TR8KH6XPZ" />{' '}
          <param name="toolbar" value="yes" />
          <param name="static_image" value="https://public.tableau.com/static/images/TR/TR8KH6XPZ/1.png" />{' '}
          <param name="animate_transition" value="yes" />
          <param name="display_static_image" value="yes" />
          <param name="display_spinner" value="yes" />
          <param name="display_overlay" value="yes" />
          <param name="display_count" value="yes" />
          <param name="language" value="en-US" />
          <param name="filter" value="SolarIrradianceByMonth%3Fpublish=yes" />
          <param name="filter" value="Latitude=1.3" />
          <param name="filter" value="Longitude=110" />
        </object>
      </div>
    </div>
  );
}

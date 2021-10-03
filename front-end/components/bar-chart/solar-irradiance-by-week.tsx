import { useEffect } from 'react';

interface Props {
  lat: number;
  lng: number;
}

export function SolarIrradianceByWeek(props: Props) {
  const { lat = 1.3, lng = 130 } = props;

  useEffect(() => {
    var divElement = document.getElementById('viz1633247930707');
    var vizElement = divElement.getElementsByTagName('object')[0];
    if (divElement.offsetWidth > 800) {
      vizElement.style.minWidth = '420px';
      vizElement.style.maxWidth = '1920px';
      vizElement.style.width = '100%';
      vizElement.style.height = '1527px';
    } else if (divElement.offsetWidth > 500) {
      vizElement.style.minWidth = '420px';
      vizElement.style.maxWidth = '1920px';
      vizElement.style.width = '100%';
      vizElement.style.height = '1527px';
    } else {
      vizElement.style.width = '100%';
      vizElement.style.height = '627px';
    }
    var scriptElement = document.createElement('script');
    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
    vizElement.parentNode.insertBefore(scriptElement, vizElement);
  }, []);

  return (
    <div>
      <div className="tableauPlaceholder" id="viz1633247930707" style={{ position: 'relative' }}>
        <noscript>
          <a href="#">
            <img
              alt="Irradiance by Week at Your Location Dashboard-NoHeader "
              src="https://public.tableau.com/static/images/MM/MMJYFPD8B/1_rss.png"
              style={{ border: 'none' }}
            />
          </a>
        </noscript>
        <object className="tableauViz" style={{ display: 'none' }}>
          <param name="host_url" value="https%3A%2F%2Fpublic.tableau.com%2F" />{' '}
          <param name="embed_code_version" value="3" /> <param name="path" value="shared/MMJYFPD8B" />{' '}
          <param name="toolbar" value="yes" />
          <param name="static_image" value="https://public.tableau.com/static/images/MM/MMJYFPD8B/1.png" />{' '}
          <param name="animate_transition" value="yes" />
          <param name="display_static_image" value="yes" />
          <param name="display_spinner" value="yes" />
          <param name="display_overlay" value="yes" />
          <param name="display_count" value="yes" />
          <param name="language" value="en-US" />
          <param name="filter" value="publish=yes" />
          <param name="filter" value={`Latitude=${lat}`} />
          <param name="filter" value={`Longitude=${lng}`} />
        </object>
      </div>
    </div>
  );
}

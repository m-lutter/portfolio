// Based on the supplied FieldPlan v21 and FieldMark2 compression-slider sources.
// Both applications were developed for, and are copyrighted by, Talman Consultants, LLC.
export const fieldTools = [
  {
    slug: 'fieldplan', title: 'FieldPlan: turn work lists into maps and driving routes',
    name: 'FieldPlan: turn work lists into maps and driving routes', artLabel: 'FieldPlan',
    category: 'software', type: 'Field planning software', status: 'Public web application',
    art: 'fieldplan', image: 'fieldplan-route-map.png', imageWidth: 1280, imageHeight: 720, cardFit: 'contain',
    caption: 'Live FieldPlan preview with 40 randomly placed synthetic Chicago work locations: 30 red and 10 yellow. All three work areas and routes are displayed, starting and finishing at Talman HQ in Westmont. Lines connect the ordered stops. Captured September 11, 2026. Map: © OpenStreetMap contributors.',
    context: 'Professional work · Talman Consultants, LLC',
    description: 'Built a Python app that combines spreadsheets and KMZ files, filters sites by work and photo readiness, partitions field assignments, and plans driving routes using road-network distances.',
    tags: ['Python', 'Streamlit', 'OR-Tools', 'Geospatial data'],
    lead: 'Developed a field-planning application for Talman Consultants, LLC that turns work lists and existing map files into organized locations, geographic assignments, and ordered driving routes.',
    role: 'Workflow design, Python development & iteration',
    outcome: 'Public Streamlit application for field planning',
    evidenceNote: 'Based on the maintained v21 Python source, synthetic checks, and live-app screenshots captured with synthetic work records on September 11, 2026.',
    sections: [
      { title: 'From work lists to field assignments', paragraphs: ['Field work starts with information spread across spreadsheets and map files. FieldPlan accepts raw Excel lists, coordinate CSV files, and existing KML/KMZ maps in one upload workflow. It combines usable locations, handles repeated labels, and preserves available map context.', 'The application applies work-completion and photo-readiness rules before export. A site with completed Thermo work and no completed-photo value becomes yellow, so it appears only when the user chooses to include photo-ready sites.'], figure: { image: 'fieldplan-project-setup.png', imageWidth: 1280, imageHeight: 720, caption: 'A synthetic HMA/PCC workbook becomes 40 combined locations and three work areas using depot-balanced sectors from Talman HQ. Random coordinates were checked against Chicago’s public community-area boundaries; the work records are fictional.' } },
      { title: 'Planning the route', paragraphs: ['Users can assign sites to existing polygons or generate geographic partitions, choose a start and finish, and route one group, all locations, or groups in a batch. OSRM provides road-network distances and travel times; Google OR-Tools calculates a stop order under the selected trip constraints.', 'The outputs include ordered CSV records, KMZ maps, and a map preview. The map lines show the stop sequence; they are overview segments rather than turn-by-turn road geometry.'], figure: { image: 'fieldplan-route-results.png', imageWidth: 1280, imageHeight: 720, caption: 'Trip summaries and ordered stops for all three groups, each returning to Talman HQ. Distances and times are estimates from this synthetic run, not measured field performance or a savings claim.' } },
      { title: 'Current implementation', paragraphs: ['The public application is available through Streamlit. Repository checks use synthetic work lists and a supplied distance matrix to check status precedence, inclusion filters, duplicate handling, route visits, and KMZ exports.', 'Routing is heuristic, and geocoding and road-service availability can affect results. No measured field-time or mileage savings are claimed.'] },
      { title: 'Ownership', paragraphs: ['Developed by Maxwell Lutter for Talman Consultants, LLC. Copyright © 2026 Talman Consultants, LLC. All rights reserved.'] }
    ],
    resources: [['Open FieldPlan', 'https://fieldplan.streamlit.app/', 'Live application']]
  },
  {
    slug: 'fieldmark2', title: 'FieldMark2: turn GPS photos into field records and maps',
    name: 'FieldMark2: turn GPS photos into field records and maps', artLabel: 'FieldMark2',
    category: 'software', type: 'Field records software', status: 'Python desktop application',
    context: 'Professional work · Talman Consultants, LLC',
    description: 'Built a desktop tool that extracts photo GPS data, matches images to poles and underground structures, combines existing CSV records, and exports Excel fielding sheets and KMZ maps.',
    tags: ['Python', 'Tkinter', 'Pillow', 'Excel / KMZ'],
    lead: 'Developed a desktop application for Talman Consultants, LLC that organizes GPS-tagged field photographs and existing CSV records into structure-based Excel sheets and mapped records.',
    role: 'Workflow design, Python development & iteration',
    outcome: 'Excel fielding records and KMZ maps from photo folders',
    evidenceNote: 'Based on the supplied compression-slider application and synthetic processing/export checks.',
    sections: [
      { title: 'Organizing the field record', paragraphs: ['FieldMark2 scans a selected folder for JPEG photographs and CSV records. It extracts GPS metadata, uses folder names to classify structures, and matches nearby compatible records. Multiple photographs can belong to one structure, with OCalc and other support photographs associated with nearby poles.', 'A review dialog collects missing conduit information or notes for applicable underground structures. The outputs combine the resulting records with photo contact sheets in Excel and embedded photographs in a KMZ map.'] },
      { title: 'Controlling output size', paragraphs: ['A five-level compression control adjusts the image copies embedded in the KMZ. Level 4 is the default, limiting ordinary images to 1024 × 768 pixels at JPEG quality 65. OCalc photographs bypass compression and remain at their original resolution.', 'Original source photos are retained. The application reports skipped and unmatched counts so missing GPS or unassociated support photos are visible at the end of processing.'] },
      { title: 'Current implementation', paragraphs: ['The maintained application uses Python and Tkinter, with Pillow for images and openpyxl for workbooks. Its repository includes installation instructions, a Windows packaging script, and clearly synthetic sample inputs.', 'Processing checks cover GPS metadata, grouping, Excel rows, KMZ image references, compression dimensions, and byte-preserved OCalc images. Proximity matching is a practical heuristic and does not establish survey accuracy.'] },
      { title: 'Ownership', paragraphs: ['Developed by Maxwell Lutter for Talman Consultants, LLC. Copyright © 2026 Talman Consultants, LLC. All rights reserved.'] }
    ],
    resources: [
      ['Source and setup instructions', 'https://github.com/m-lutter/FieldMark2', 'GitHub'],
      ['Processing and export checks', 'https://github.com/m-lutter/FieldMark2/tree/main/tests', 'Tests']
    ]
  }
];

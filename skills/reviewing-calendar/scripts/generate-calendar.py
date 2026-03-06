#!/usr/bin/env python3
"""
Generates a Google Calendar-style dark-themed HTML weekly view from event JSON.
Reads JSON array of events from stdin, writes HTML to stdout.

Event format:
{
  "id": "...",
  "summary": "...",
  "start": "2026-03-02T12:00:00-08:00" or "2026-03-02" (all-day),
  "end": "2026-03-02T12:30:00-08:00" or "2026-03-03" (all-day),
  "organizer": "username",
  "optional": false
}
"""

import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict

def parse_events():
    raw = json.load(sys.stdin)
    events = []
    for e in raw:
        start_str = e.get("start", "")
        end_str = e.get("end", "")
        # Detect all-day (date only, no T)
        all_day = "T" not in start_str
        cancelled = "Cancelled" in e.get("summary", "") or "OUTDATED" in e.get("summary", "")
        events.append({
            "id": e.get("id", ""),
            "summary": e.get("summary", "(no title)"),
            "start": start_str,
            "end": end_str,
            "organizer": e.get("organizer", "").split("@")[0] if "@" in e.get("organizer", "") else e.get("organizer", ""),
            "optional": e.get("optional", False),
            "allDay": all_day,
            "cancelled": cancelled,
        })
    return events

def get_weeks(events):
    """Group events into Mon-Fri weeks."""
    all_dates = set()
    for e in events:
        s = e["start"][:10]
        try:
            d = datetime.strptime(s, "%Y-%m-%d")
            all_dates.add(d)
        except:
            pass
    if not all_dates:
        return []

    min_d = min(all_dates)
    max_d = max(all_dates)
    # Align to Monday
    start_monday = min_d - timedelta(days=min_d.weekday())
    end_friday = max_d + timedelta(days=(4 - max_d.weekday()) % 7) if max_d.weekday() <= 4 else max_d - timedelta(days=max_d.weekday() - 4)

    weeks = []
    current = start_monday
    while current <= end_friday:
        days = []
        for i in range(5):  # Mon-Fri
            d = current + timedelta(days=i)
            days.append({
                "dow": ["MON", "TUE", "WED", "THU", "FRI"][i],
                "dom": d.day,
                "date": d.strftime("%Y-%m-%d"),
            })
        fri = current + timedelta(days=4)
        weeks.append({
            "label": f"Week of {current.strftime('%B')} {current.day} – {fri.day}, {current.year}",
            "days": days,
        })
        current += timedelta(weeks=1)

    return weeks

def generate_html(events, weeks, title="Calendar Events"):
    events_json = json.dumps(events)
    weeks_json = json.dumps(weeks)
    count = len(events)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#1d1d1d;color:#e8eaed;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;font-size:14px}}
.header{{padding:16px 24px;border-bottom:1px solid #3c4043;display:flex;align-items:center;gap:16px}}
.header h1{{font-size:22px;font-weight:400;color:#e8eaed}}
.header .badge{{background:#039BE5;color:#fff;border-radius:12px;padding:2px 10px;font-size:12px;font-weight:500}}
.header .subtitle{{color:#9aa0a6;font-size:13px}}
.week-section{{padding:8px 0}}
.week-label{{padding:8px 24px;font-size:13px;font-weight:500;color:#8ab4f8;text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid #3c4043}}
.cal-container{{display:flex;position:relative}}
.time-gutter{{width:72px;flex-shrink:0}}
.time-label{{height:60px;padding-right:12px;text-align:right;font-size:11px;color:#9aa0a6;line-height:1;position:relative;top:-6px}}
.days-header{{display:flex;flex:1}}
.day-header{{flex:1;text-align:center;padding:8px 0;border-bottom:1px solid #3c4043;border-left:1px solid #3c4043}}
.day-header .dow{{font-size:11px;color:#9aa0a6;text-transform:uppercase;letter-spacing:0.5px}}
.day-header .dom{{font-size:24px;color:#e8eaed;margin-top:2px}}
.allday-row{{display:flex;min-height:28px;border-bottom:1px solid #3c4043}}
.allday-gutter{{width:72px;flex-shrink:0;font-size:11px;color:#9aa0a6;text-align:right;padding:4px 12px 4px 0}}
.allday-cell{{flex:1;border-left:1px solid #3c4043;padding:2px 4px}}
.allday-event{{background:#1B5E20;color:#A5D6A7;border-radius:4px;padding:2px 8px;font-size:11px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:2px}}
.grid-body{{display:flex;flex:1;position:relative}}
.grid-col{{flex:1;border-left:1px solid #3c4043;position:relative}}
.grid-col .hour-line{{height:60px;border-bottom:1px solid #303030}}
.event-block{{position:absolute;left:2px;right:2px;border-radius:4px;padding:4px 8px;overflow:hidden;cursor:pointer;z-index:2;transition:box-shadow 0.15s;font-size:12px;line-height:1.3}}
.event-block:hover{{box-shadow:0 4px 12px rgba(0,0,0,0.5);z-index:10}}
.event-block .ev-title{{font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.event-block .ev-time{{font-size:11px;opacity:0.85;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.event-block .ev-org{{font-size:10px;opacity:0.6;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.event-block.required{{background:#039BE5;color:#fff}}
.event-block.optional{{background:#546E7A;color:#CFD8DC}}
.event-block.cancelled{{background:#4a2020;color:#EF9A9A;text-decoration:line-through}}
.event-block.conflict{{border-left:3px solid #EF5350}}
.tooltip{{display:none;position:fixed;background:#303134;border:1px solid #5f6368;border-radius:8px;padding:12px 16px;z-index:100;max-width:320px;box-shadow:0 8px 24px rgba(0,0,0,0.6);pointer-events:none}}
.tooltip .tt-title{{font-size:14px;font-weight:500;margin-bottom:4px}}
.tooltip .tt-time,.tooltip .tt-org{{font-size:12px;color:#9aa0a6;margin-bottom:2px}}
.tooltip .tt-badge{{display:inline-block;font-size:10px;padding:1px 6px;border-radius:4px;margin-top:4px}}
.tt-badge.opt{{background:#546E7A;color:#CFD8DC}}
.tt-badge.req{{background:#039BE5;color:#fff}}
.legend{{display:flex;gap:20px;padding:12px 24px;border-top:1px solid #3c4043;font-size:12px;color:#9aa0a6;align-items:center;flex-wrap:wrap}}
.legend-item{{display:flex;align-items:center;gap:6px}}
.legend-swatch{{width:14px;height:14px;border-radius:3px}}
</style>
</head>
<body>
<div class="header">
  <h1>{title}</h1>
  <span class="badge">{count}</span>
</div>
<div id="cal-root"></div>
<div class="legend">
  <div class="legend-item"><div class="legend-swatch" style="background:#039BE5"></div> Required</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#546E7A"></div> Optional</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#4a2020"></div> Cancelled/Outdated</div>
  <div class="legend-item"><div class="legend-swatch" style="background:transparent;border-left:3px solid #EF5350;width:8px"></div> Conflict</div>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
const events={events_json};
const weeks={weeks_json};
const HOUR_H=60,START_HOUR=8,END_HOUR=17,HOURS=END_HOUR-START_HOUR;

function fmtTime(d){{let h=d.getHours(),m=d.getMinutes(),ap=h>=12?'pm':'am';h=h%12||12;return m?h+':'+String(m).padStart(2,'0')+ap:h+ap;}}
function getEventsForDate(ds){{return events.filter(e=>!e.allDay&&e.start.substring(0,10)===ds);}}
function getAllDayForWeek(w){{return events.filter(e=>{{if(!e.allDay)return false;const es=new Date(e.start),ee=new Date(e.end),ws=new Date(w.days[0].date),we=new Date(w.days[4].date);we.setDate(we.getDate()+1);return es<we&&ee>ws;}});}}
function detectConflicts(devs){{const s=[...devs].sort((a,b)=>new Date(a.start)-new Date(b.start));const c=new Set();for(let i=0;i<s.length;i++)for(let j=i+1;j<s.length;j++)if(new Date(s[i].end)>new Date(s[j].start)){{c.add(s[i].id);c.add(s[j].id);}}return c;}}
function layoutOverlaps(devs){{const s=[...devs].sort((a,b)=>new Date(a.start)-new Date(b.start));const cols=[];const cm=new Map();for(const ev of s){{let placed=false;for(let c=0;c<cols.length;c++){{if(new Date(cols[c][cols[c].length-1].end)<=new Date(ev.start)){{cols[c].push(ev);cm.set(ev.id,c);placed=true;break;}}}}if(!placed){{cols.push([ev]);cm.set(ev.id,cols.length-1);}}}}return {{colMap:cm,totalCols:cols.length}};}}

const root=document.getElementById('cal-root'),tooltip=document.getElementById('tooltip');
weeks.forEach(week=>{{
  const section=document.createElement('div');section.className='week-section';
  const label=document.createElement('div');label.className='week-label';label.textContent=week.label;section.appendChild(label);
  const hr=document.createElement('div');hr.style.display='flex';
  const gh=document.createElement('div');gh.style.width='72px';gh.style.flexShrink='0';hr.appendChild(gh);
  const dh=document.createElement('div');dh.className='days-header';
  week.days.forEach(d=>{{const el=document.createElement('div');el.className='day-header';el.innerHTML='<div class="dow">'+d.dow+'</div><div class="dom">'+d.dom+'</div>';dh.appendChild(el);}});
  hr.appendChild(dh);section.appendChild(hr);
  const adEvs=getAllDayForWeek(week);
  if(adEvs.length){{const ar=document.createElement('div');ar.className='allday-row';const ag=document.createElement('div');ag.className='allday-gutter';ag.textContent='all-day';ar.appendChild(ag);
  week.days.forEach(d=>{{const cell=document.createElement('div');cell.className='allday-cell';adEvs.forEach(e=>{{const es=new Date(e.start),ee=new Date(e.end),cd=new Date(d.date);cd.setHours(12);if(cd>=es&&cd<ee){{const p=document.createElement('div');p.className='allday-event';p.textContent=e.summary;cell.appendChild(p);}}}});ar.appendChild(cell);}});section.appendChild(ar);}}
  const ct=document.createElement('div');ct.className='cal-container';
  const gt=document.createElement('div');gt.className='time-gutter';
  for(let h=START_HOUR;h<END_HOUR;h++){{const tl=document.createElement('div');tl.className='time-label';tl.textContent=(h%12||12)+' '+(h>=12?'PM':'AM');gt.appendChild(tl);}}
  ct.appendChild(gt);
  const bd=document.createElement('div');bd.className='grid-body';
  week.days.forEach(d=>{{const col=document.createElement('div');col.className='grid-col';
  for(let h=0;h<HOURS;h++){{const hl=document.createElement('div');hl.className='hour-line';col.appendChild(hl);}}
  const devs=getEventsForDate(d.date);const conflicts=detectConflicts(devs);const {{colMap,totalCols}}=layoutOverlaps(devs);
  devs.forEach(ev=>{{const s=new Date(ev.start),e=new Date(ev.end);const sm=(s.getHours()-START_HOUR)*60+s.getMinutes();const dur=Math.max((e.getHours()-START_HOUR)*60+e.getMinutes()-sm,20);
  const top=(sm/60)*HOUR_H,height=(dur/60)*HOUR_H;const ci=colMap.get(ev.id)||0;const wp=100/totalCols;
  const bl=document.createElement('div');bl.className='event-block';
  if(ev.cancelled)bl.classList.add('cancelled');else if(ev.optional)bl.classList.add('optional');else bl.classList.add('required');
  if(conflicts.has(ev.id))bl.classList.add('conflict');
  bl.style.top=top+'px';bl.style.height=height+'px';
  if(totalCols>1){{bl.style.left=wp*ci+'%';bl.style.width='calc('+wp+'% - 4px)';bl.style.right='auto';}}
  bl.innerHTML='<div class="ev-title">'+ev.summary+'</div><div class="ev-time">'+fmtTime(s)+' – '+fmtTime(e)+'</div>'+(height>40?'<div class="ev-org">'+ev.organizer+'</div>':'');
  bl.addEventListener('mouseenter',function(me){{tooltip.innerHTML='<div class="tt-title">'+ev.summary+'</div><div class="tt-time">📅 '+fmtTime(s)+' – '+fmtTime(e)+'</div><div class="tt-org">👤 '+ev.organizer+'</div>'+(conflicts.has(ev.id)?'<div style="color:#EF5350;font-size:11px;margin-top:4px">⚠️ Conflicts with another event</div>':'')+(ev.cancelled?'<div style="color:#EF9A9A;font-size:11px;margin-top:4px">❌ Cancelled/Outdated</div>':'')+'<span class="tt-badge '+(ev.optional?'opt':'req')+'">'+(ev.optional?'Optional':'Required')+'</span>';tooltip.style.display='block';const r=bl.getBoundingClientRect();tooltip.style.left=(r.right+8)+'px';tooltip.style.top=r.top+'px';}});
  bl.addEventListener('mouseleave',()=>{{tooltip.style.display='none'}});
  col.appendChild(bl);}});bd.appendChild(col);}});
  ct.appendChild(bd);section.appendChild(ct);root.appendChild(section);
}});
</script>
</body>
</html>"""


if __name__ == "__main__":
    events = parse_events()
    weeks = get_weeks(events)
    title = sys.argv[1] if len(sys.argv) > 1 else "Pending Calendar Invites — Needs Response"
    print(generate_html(events, weeks, title))

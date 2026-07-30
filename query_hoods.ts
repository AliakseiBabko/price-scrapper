import { initDb, db } from './src/database/db.js';
import fs from 'fs';

initDb();

const brands = ['bosch', 'electrolux', 'gorenje'];
const output: Record<string, any[]> = {};

for (const brand of brands) {
  const products = db.prepare(`
    SELECT p.id, p.brand, p.title, p.model, p.rating, p.reviews_count, p.specs_json,
           MIN(o.price) as min_price
    FROM products p
    LEFT JOIN offers o ON o.product_id = p.id
    WHERE p.category_id = 'hoods'
      AND LOWER(p.brand) = ?
    GROUP BY p.id
    ORDER BY min_price ASC NULLS LAST
  `).all(brand) as any[];

  const get = (specs: Record<string, string>, ...keys: string[]) => {
    for (const k of keys) {
      if (specs[k] && specs[k] !== 'N/A' && !specs[k].startsWith(k)) return specs[k];
    }
    return '—';
  };

  output[brand] = products.map(p => {
    let specs: Record<string, string> = {};
    try { specs = JSON.parse(p.specs_json || '{}'); } catch {}

    return {
      id: p.id,
      title: p.title,
      model: p.model,
      price: p.min_price ? Math.round(Number(p.min_price)) : null,
      mount: get(specs, 'Монтаж', 'Способ установки', 'Тип'),
      capacity: get(specs, 'Максимальная производительность отвода', 'Производительность', 'Номинальная производительность'),
      capacity_min: get(specs, 'Минимальная производительность отвода'),
      noise_max: get(specs, 'Максимальный уровень шума'),
      noise_min: get(specs, 'Минимальный уровень шума'),
      color: get(specs, 'Цвет', 'Цвет корпуса'),
      width: get(specs, 'Ширина'),
      control: get(specs, 'Управление', 'Тип управления'),
      duct: get(specs, 'Диаметр воздуховода'),
      motors: get(specs, 'Количество моторов'),
      perimetral: get(specs, 'Периметральное воздухопоглощение'),
      wifi: get(specs, 'Удаленное управление (Wi-Fi)'),
      remote: get(specs, 'Пульт ДУ'),
      energy: get(specs, 'Энергоэффективность'),
      motor_power: get(specs, 'Мощность мотора'),
    };
  });
}

fs.writeFileSync('./scratch/hood_data.json', JSON.stringify(output, null, 2));
console.log('Saved to scratch/hood_data.json');

// Print structured summary
for (const [brand, models] of Object.entries(output)) {
  console.log(`\n${'='.repeat(80)}`);
  console.log(`${brand.toUpperCase()}`);
  for (const m of models) {
    console.log(`\n  ${m.title}`);
    console.log(`  Price: ${m.price ?? 'N/A'} BYN | Mount: ${m.mount} | Width: ${m.width} | Duct: ${m.duct}`);
    console.log(`  Capacity max: ${m.capacity} | min: ${m.capacity_min}`);
    console.log(`  Noise max: ${m.noise_max} | min: ${m.noise_min}`);
    console.log(`  Color: ${m.color} | Control: ${m.control} | Motors: ${m.motors}`);
    console.log(`  Perimetral: ${m.perimetral} | WiFi: ${m.wifi} | Remote: ${m.remote} | Energy: ${m.energy}`);
  }
}

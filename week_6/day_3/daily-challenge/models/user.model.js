import db from '../config/database.js';

const User = {
  create: (data, trx = null) => (trx ? db('users').transacting(trx).insert(data).returning('*') : db('users').insert(data).returning('*')),
  findAll: () => db('users').select('*'),
  findById: (id) => db('users').where({ id }).first(),
  update: (id, data, trx = null) => (trx ? db('users').where({ id }).transacting(trx).update(data).returning('*') : db('users').where({ id }).update(data).returning('*')),
  delete: (id) => db('users').where({ id }).del(),
};

export default User;
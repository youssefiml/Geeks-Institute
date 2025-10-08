import db from '../config/database.js';

const HashPwd = {
  create: (data, trx = null) => (trx ? db('hashpwds').transacting(trx).insert(data).returning('*') : db('hashpwds').insert(data).returning('*')),
  findByUsername: (username) => db('hashpwds').where({ username }).first(),
  updatePassword: (id, password, trx = null) => (trx ? db('hashpwds').where({ id }).transacting(trx).update({ password }).returning('*') : db('hashpwds').where({ id }).update({ password }).returning('*')),
};

export default HashPwd;
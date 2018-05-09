UPDATE std_bounties_bounty
SET platform = 'bounties-network'
WHERE platform is NULL
AND bounty_created < '2018-05-09T18:45:52.383Z';

UPDATE std_bounties_fulfillment
SET platform = 'bounties-network'
WHERE platform is NULL
AND fulfillment_created < '2018-05-09T18:45:52.383Z';

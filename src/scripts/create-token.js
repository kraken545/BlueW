#!/usr/bin/env node
/**
 * BlueWave - Token Creation Script (Token-2022 con 2% Transfer Fee)
 * Uso: node src/scripts/create-token.js
 *
 * Requisitos:
 *   npm install @solana/web3.js @solana/spl-token
 *   Tener SOL en la wallet para comisiones
 *   Editar las constantes abajo
 */

const {
  Connection, Keypair, PublicKey, Transaction, SystemProgram,
  sendAndConfirmTransaction, LAMPORTS_PER_SOL,
} = require("@solana/web3.js");
const {
  createInitializeTransferFeeConfigInstruction,
  createInitializeMintInstruction,
  getMintLen,
  TOKEN_2022_PROGRAM_ID,
  ExtensionType,
} = require("@solana/spl-token");
const fs = require("fs");
const path = require("path");

// ===========================
// CONFIGURACIÓN - CÁMBIAME
// ===========================
const RPC_URL = "https://api.devnet.solana.com"; // devnet para pruebas
const MARKETING_WALLET = new PublicKey("11111111111111111111111111111111"); // Cámbialo a tu wallet marketing
const KEYPAIR_PATH = path.join(require("os").homedir(), ".config/solana/id.json");
// ===========================

async function main() {
  console.log("🚀 BlueWave Token Creator");
  console.log(`   Network: ${RPC_URL}`);
  console.log("");

  // 1. Cargar wallet
  if (!fs.existsSync(KEYPAIR_PATH)) {
    console.error(`❌ No se encontró wallet en: ${KEYPAIR_PATH}`);
    console.error("   Crea una con: solana-keygen new");
    process.exit(1);
  }
  const secretKey = Uint8Array.from(JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf8")));
  const payer = Keypair.fromSecretKey(secretKey);
  console.log(`   Payer: ${payer.publicKey.toBase58()}`);

  const connection = new Connection(RPC_URL, "confirmed");

  // 2. Balance check
  const balance = await connection.getBalance(payer.publicKey);
  console.log(`   Balance: ${balance / LAMPORTS_PER_SOL} SOL`);
  if (balance < 0.01 * LAMPORTS_PER_SOL) {
    console.error("❌ Balance muy bajo. Necesitas al menos 0.01 SOL");
    process.exit(1);
  }

  // 3. Generar keypair para el token mint
  const mintKeypair = Keypair.generate();
  const mint = mintKeypair.publicKey;
  console.log(`   New Mint: ${mint.toBase58()}`);

  // 4. Calcular espacio para el mint con extensiones
  const mintLen = getMintLen([ExtensionType.TransferFeeConfig]);
  const lamports = await connection.getMinimumBalanceForRentExemption(mintLen);
  console.log(`   Rent: ${lamports} lamports | Mint size: ${mintLen} bytes`);

  // 5. Construir transacción
  const tx = new Transaction();

  // 5a. Crear cuenta del mint
  tx.add(
    SystemProgram.createAccount({
      fromPubkey: payer.publicKey,
      newAccountPubkey: mint,
      space: mintLen,
      lamports,
      programId: TOKEN_2022_PROGRAM_ID,
    })
  );

  // 5b. Configurar TransferFee (2% = 200 basis points)
  // transferFeeBasisPoints: 200 = 2%
  // maxFee: 1,000,000,000 (1 SOL en lamports) máximo de tax por transferencia
  const transferFeeBasisPoints = 200;
  const maxFee = BigInt(1_000_000_000_000);
  tx.add(
    createInitializeTransferFeeConfigInstruction(
      mint,
      TOKEN_2022_PROGRAM_ID,
      payer.publicKey,           // authority que puede cambiar la config
      MARKETING_WALLET,          // wallet que recibe las fees
      transferFeeBasisPoints,
      maxFee,
    )
  );

  // 5c. Inicializar Mint (6 decimales)
  const decimals = 6;
  tx.add(
    createInitializeMintInstruction(
      mint,
      decimals,
      payer.publicKey,  // mint authority
      null,             // freeze authority
      TOKEN_2022_PROGRAM_ID,
    )
  );

  // 6. Firmar y enviar
  tx.feePayer = payer.publicKey;
  tx.recentBlockhash = (await connection.getLatestBlockhash()).blockhash;
  tx.sign(payer, mintKeypair);

  console.log("⏳ Enviando transacción...");
  const sig = await sendAndConfirmTransaction(connection, tx, [payer, mintKeypair]);
  console.log("");
  console.log("✅ Token creado exitosamente!");
  console.log(`   Signature: ${sig}`);
  console.log(`   Mint: ${mint.toBase58()}`);
  console.log(`   Explorador: https://solscan.io/token/${mint.toBase58()}?cluster=devnet`);
  console.log("");
  console.log("📝 Detalles del token:");
  console.log(`   Name: BlueWave`);
  console.log(`   Symbol: BLUEW`);
  console.log(`   Decimals: ${decimals}`);
  console.log(`   Supply: 1,000,000,000`);
  console.log(`   Tax: 2% a ${MARKETING_WALLET.toBase58()}`);
  console.log(`   Standard: SPL Token-2022`);
}

main().catch(console.error);

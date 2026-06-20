import {
  Connection, Keypair, PublicKey, Transaction, sendAndConfirmTransaction
} from "@solana/web3.js";
import {
  createInitializeTransferFeeConfigInstruction,
  createInitializeMintInstruction,
  getMintLen,
  TOKEN_2022_PROGRAM_ID,
  ExtensionType,
  createInitializeMetadataPointerInstruction,
} from "@solana/spl-token";
import { createInitializeInstruction, pack } from "@solana/spl-token-metadata";
import fs from "fs";
import path from "path";

// ===========================
// CONFIG - CÁMBIA ESTO
// ===========================
const RPC_URL = "https://api.mainnet-beta.solana.com"; // o devnet para pruebas
const MARKETING_WALLET = "TU_WALLET_DE_MARKETING_AQUI"; // wallet que recibe el 2%
const KEYPAIR_PATH = path.join(process.env.HOME || "~", ".config/solana/id.json");
// ===========================

async function main() {
  const connection = new Connection(RPC_URL, "confirmed");

  // Cargar keypair del creador
  const keypairBytes = JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf-8"));
  const creator = Keypair.fromSecretKey(Uint8Array.from(keypairBytes));

  console.log(`Creador: ${creator.publicKey.toBase58()}`);

  // Generar nueva keypair para el mint del token
  const mintKeypair = Keypair.generate();
  const mint = mintKeypair.publicKey;

  console.log(`Mint address: ${mint.toBase58()}`);

  // Metadata del token
  const tokenMetadata = {
    mint,
    name: "BlueWave",
    symbol: "BLUEW",
    uri: "https://raw.githubusercontent.com/tu-user/tu-repo/main/metadata/token.json",
    additionalMetadata: [["description", "BlueWave - Good vibes & tourism from Curaçao"]],
  };

  // Calcular tamaño con extensiones: TransferFeeConfig + MetadataPointer + TokenMetadata
  const transferFeeConfigSize = ExtensionType.TransferFeeConfig;
  const metadataPointerSize = ExtensionType.MetadataPointer;
  const tokenMetadataSize = ExtensionType.TokenMetadata;

  const mintLen = getMintLen([
    transferFeeConfigSize,
    metadataPointerSize,
  ]);

  // Tamaño extra para los metadatos inline
  const metaData = pack(tokenMetadata);
  const totalLen = mintLen + metaData.length;

  // Lamports para rent-exempt
  const lamports = await connection.getMinimumBalanceForRentExemption(totalLen);

  // Construir TX
  const tx = new Transaction();

  // 1. Cuenta mint
  tx.add(
    SystemProgram.createAccount({
      fromPubkey: creator.publicKey,
      newAccountPubkey: mint,
      space: totalLen,
      lamports,
      programId: TOKEN_2022_PROGRAM_ID,
    })
  );

  // 2. Inicializar TransferFeeConfig (2% - 200 bps)
  // TransferFeeConfig: transfer_fee_basis_points = 200 (2%), max_fee = 1_000_000_000_000
  const transferFeeBasisPoints = 200; // 2% en bps
  const maxFee = 1_000_000_000_000n; // máximo fee en smallest unit
  const transferFeeInstruction = createInitializeTransferFeeConfigInstruction(
    mint,
    TOKEN_2022_PROGRAM_ID,
    creator.publicKey, // authority que puede modificar la config (podria ser null)
    marketingWallet,   // wallet que recibe los fees recogidos
    transferFeeBasisPoints,
    maxFee,
  );
  tx.add(transferFeeInstruction);

  // 3. Inicializar MetadataPointer
  tx.add(
    createInitializeMetadataPointerInstruction(
      mint,
      undefined, // autoridad de la metadata (mint authority por defecto)
      mint,
      TOKEN_2022_PROGRAM_ID,
    )
  );

  // 4. Inicializar TokenMetadata inline
  tx.add(
    createInitializeInstruction({
      programId: TOKEN_2022_PROGRAM_ID,
      metadata: mint,
      updateAuthority: creator.publicKey,
      mint: mint,
      mintAuthority: creator.publicKey,
      name: tokenMetadata.name,
      symbol: tokenMetadata.symbol,
      uri: tokenMetadata.uri,
    })
  );

  // 5. Inicializar Mint
  const decimals = 6;
  tx.add(
    createInitializeMintInstruction(
      mint,
      decimals,
      creator.publicKey, // mint authority
      null,              // freeze authority
      TOKEN_2022_PROGRAM_ID,
    )
  );

  // Firmar y enviar
  tx.feePayer = creator.publicKey;
  tx.recentBlockhash = (await connection.getRecentBlockhash()).blockhash;
  tx.sign(mintKeypair, creator);

  const sig = await sendAndConfirmTransaction(connection, tx, [mintKeypair, creator]);
  console.log(`Token creado: ${sig}`);
  console.log(`Mint address: ${mint.toBase58()}`);
  console.log(`Explorador: https://solscan.io/token/${mint.toBase58()}`);
}

main().catch(console.error);
